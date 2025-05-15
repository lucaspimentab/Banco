import json
import os
import requests
from datetime import datetime
from app.cliente import Cliente
from app.conta_corrente import ContaCorrente
from app.conta_poupanca import ContaPoupanca


class Banco:
    def __init__(self):
        self.clientes = []

    def abrir_conta(
            self, 
            tipo_conta, 
            nome, 
            cpf, 
            telefone, 
            email, 
            cep, 
            numero_endereco, 
            senha, 
            data_nascimento
        ):
        mensagens = []

        # Verificar idade mínima
        try:
            nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
            idade = (datetime.now() - nascimento).days // 365
            if idade < 18:
                mensagens.append("Usuário deve ter pelo menos 18 anos.")
        except Exception:
            mensagens.append("Data de nascimento inválida. Use o formato YYYY-MM-DD.")

        # Consulta o CEP usando a API ViaCEP
        try:
            cep_limpo = cep.replace("-", "").strip()
            response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/")
            data = response.json()

            if "erro" in data:
                mensagens.append("CEP inválido ou não encontrado.")
            else:
                logradouro = data.get("logradouro", "")
                bairro = data.get("bairro", "")
                cidade = data.get("localidade", "")
                estado = data.get("uf", "")
                endereco = f"{logradouro}, {numero_endereco}, {bairro} - {cidade}/{estado}"
        except Exception as e:
            mensagens.append(f"Erro ao buscar CEP: {str(e)}")

        if mensagens:
            return {"sucesso": False, "mensagens": mensagens}

        cliente_existente = self.buscar_cliente_por_cpf(cpf)
        if cliente_existente:
            # Verificar se já tem uma conta do mesmo tipo
            for conta in cliente_existente.contas:
                if conta.tipo.lower() == tipo_conta.lower():
                    return {"sucesso": False, "mensagens": ["CPF já possui conta desse tipo."]}

            # Validar se os dados inseridos batem com os dados existentes
            if cliente_existente.nome != nome or cliente_existente.email != email or cliente_existente.telefone != telefone or cliente_existente.senha != senha or cliente_existente.data_nascimento != data_nascimento:
                return {"sucesso": False, "mensagens": ["Os dados informados não correspondem ao cliente já existente com este CPF."]}

            cliente = cliente_existente
        else:
            cliente = Cliente(nome, cpf, data_nascimento, email, endereco, telefone, senha)
            self.clientes.append(cliente)

        tipo_conta = tipo_conta.lower()
        if tipo_conta == "corrente":
            ContaCorrente(cliente)
        elif tipo_conta == "poupanca":
            ContaPoupanca(cliente)
        else:
            return {"sucesso": False, "mensagens": ["Tipo de conta inválido."]}

        return {"sucesso": True, "cliente": cliente}

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def buscar_conta_por_numero(self, numero_conta):
        for cliente in self.clientes:
            conta = cliente.buscar_conta(numero_conta)
            if conta:
                return conta
        return None

    def salvar_dados(self, caminho):
        dados = []
        for cliente in self.clientes:
            contas = []
            for conta in cliente.contas:
                contas.append({
                    "numero": conta.numero_conta,
                    "tipo": conta.tipo,
                    "saldo": conta.saldo
                })
            
            dados.append({
                "id"              : cliente.id,
                "nome"            : cliente.nome,
                "cpf"             : cliente.cpf,
                "email"           : cliente.email,
                "data_nascimento" : cliente.data_nascimento,
                "endereco"        : cliente.endereco,
                "telefone"        : cliente.telefone,
                "data_cadastro"   : cliente.data_cadastro,
                "senha"           : cliente.senha,
                "contas"          : contas
            })

        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def carregar_dados(self, caminho):
        if not os.path.exists(caminho):
            return
        self.clientes.clear()

        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        for cliente_dado in dados:
            cliente = Cliente(
                cliente_dado["nome"],
                cliente_dado["cpf"],
                cliente_dado["data_nascimento"],
                cliente_dado["email"],
                cliente_dado["endereco"],
                cliente_dado["telefone"],
                cliente_dado.get("senha", None)
            )
            cliente.id = cliente_dado["id"]
            cliente.data_cadastro = cliente_dado["data_cadastro"]

            for conta in cliente_dado["contas"]:
                if conta["tipo"].lower() == "corrente":
                    ContaCorrente(cliente, conta["saldo"])
                else:
                    ContaPoupanca(cliente, conta["saldo"])

            self.clientes.append(cliente)