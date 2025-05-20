import datetime
import re

class Cliente:
    contador_id = 1  # Contador global associado a cada novo cliente

    def __init__(self, nome, cpf, data_nascimento, email, endereco, telefone, senha):
        """
        Inicializa um novo cliente com os dados fornecidos, atribuindo um ID único
        e registrando a data de cadastro.
        """
        self.id = Cliente.contador_id
        Cliente.contador_id += 1
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.email = self.validar_email(email)
        self.cpf = cpf
        self._senha = senha              # 🔒 senha privada
        self._contas = []                # 🔒 contas privadas
        self.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def validar_email(self, email):
        if not self.verificar_email(email):
            print(f"Erro: E-mail {email} inválido")
            return None
        return email

    def criar_senha(self, senha_criada):
        if len(senha_criada) < 9:
            return False

        tem_num = any(c.isdigit() for c in senha_criada)
        tem_letra = any(c.isalpha() for c in senha_criada)
        tem_caractere = any(c in r"!@#$%^&*(),.?/:{~}[]<>" for c in senha_criada)

        return tem_num and tem_letra and tem_caractere

    def verificar_senha(self, senha_inserida):
        return self._senha == senha_inserida

    def verificar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))

    def atualizar_dados(self, campo, dado_atualizado):
        if campo == "nome":
            self.nome = dado_atualizado
        elif campo == "data de nascimento":
            self.data_nascimento = dado_atualizado
        elif campo == "telefone":
            self.telefone = dado_atualizado
        elif campo == "endereco":
            self.endereco = dado_atualizado
        elif campo == "email":
            self.email = dado_atualizado
            if not self.verificar_email(self.email):
                self.email = ""
                return {"sucesso": False, "mensagem": f"E-mail {self.email} inválido."}
        else:
            return {"sucesso": False, "mensagem": f"Campo {campo} não reconhecido."}

        return {"sucesso": True, "mensagem": f"Campo {campo} atualizado com sucesso."}

    def adicionar_conta(self, conta):
        self._contas.append(conta)
        return {"sucesso": True, "mensagem": f"Conta {conta.numero_conta} adicionada ao cliente {self.nome}."}

    def remover_conta(self, numero_conta):
        for i in range(len(self._contas)):
            if self._contas[i].numero == numero_conta:
                conta_removida = self._contas.pop(i)
                return {"sucesso": True, "mensagem": f"Conta {numero_conta} removida do cliente {self.nome}."}
        return {"sucesso": False, "mensagem": f"Conta {numero_conta} não encontrada."}

    def buscar_conta(self, numero_conta):
        for conta in self._contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None

    def listar_contas(self):
        if len(self._contas) == 0:
            return {"sucesso": True, "mensagem": f"Cliente {self.nome} não possui contas.", "contas": []}

        print(f"Contas do cliente {self.nome}:")
        lista_contas = []
        for conta in self._contas:
            print(f"- Conta {conta.numero_conta}, Tipo: {conta.tipo}, Saldo: R$ {conta.saldo:.2f}")
            info_conta = {
                "numero": conta.numero_conta,
                "tipo": conta.tipo,
                "saldo": conta.saldo
            }
            lista_contas.append(info_conta)

        return lista_contas

    @property
    def contas(self):
        """
        Permite acesso somente leitura às contas.
        """
        return self._contas.copy()