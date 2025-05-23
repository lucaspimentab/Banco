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
        self.contas = []
        self.senha = senha
        data_atual = datetime.datetime.now()
        self.data_cadastro = data_atual.strftime("%Y-%m-%d %H:%M:%S")

    def validar_email(self, email):
        """
        Valida o formato do e-mail. Retorna o e-mail se válido, ou None se inválido.
        """
        if not self.verificar_email(email):
            print(f"Erro: E-mail {email} inválido")
            return None
        return email

    def criar_senha(self, senha_criada):
        """
        Verifica se a senha criada atende aos critérios mínimos:
        - Pelo menos 9 caracteres
        - Contém número, letra e caractere especial
        """
        if len(senha_criada) < 9:
            return False

        tem_num = False
        tem_letra = False
        tem_caractere = False
        caracteres_especiais = r"!@#$%^&*(),.?/:{~}[]<>"

        for i in senha_criada:
            if i.isdigit():
                tem_num = True
            elif i.isalpha():
                tem_letra = True
            elif i in caracteres_especiais:
                tem_caractere = True

        return tem_num and tem_letra and tem_caractere

    def verificar_senha(self, senha_inserida):
        """
        Verifica se a senha inserida é igual à senha registrada do cliente.
        """
        return self.senha == senha_inserida

    def verificar_email(self, email):
        """
        Verifica se o e-mail possui o formato válido usando expressão regular.
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))

    def atualizar_dados(self, campo, dado_atualizado):
        """
        Atualiza o campo especificado do cliente com o novo valor fornecido.
        Retorna um dicionário indicando sucesso ou erro.
        """
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
        """
        Associa uma nova conta ao cliente.
        """
        self.contas.append(conta)
        return {"sucesso": True, "mensagem": f"Conta {conta.numero_conta} adicionada ao cliente {self.nome}."}

    def remover_conta(self, numero_conta):
        """
        Remove uma conta da lista de contas do cliente, dado o número da conta.
        Retorna mensagem de sucesso ou erro.
        """
        for i in range(len(self.contas)):
            if self.contas[i].numero == numero_conta:
                conta_removida = self.contas.pop(i)
                return {"sucesso": True, "mensagem": f"Conta {numero_conta} removida do cliente {self.nome}."}
        return {"sucesso": False, "mensagem": f"Conta {numero_conta} não encontrada."}

    def buscar_conta(self, numero_conta):
        """
        Retorna a conta do cliente com o número especificado, se encontrada.
        """
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None

    def listar_contas(self):
        """
        Retorna uma lista de dicionários com os dados das contas do cliente.
        Também imprime as contas no console.
        """
        if len(self.contas) == 0:
            return {"sucesso": True, "mensagem": f"Cliente {self.nome} não possui contas.", "contas": []}

        print(f"Contas do cliente {self.nome}:")
        lista_contas = []
        for conta in self.contas:
            print(f"- Conta {conta.numero_conta}, Tipo: {conta.tipo}, Saldo: R$ {conta.saldo:.2f}")
            info_conta = {
                "numero": conta.numero_conta,
                "tipo": conta.tipo,
                "saldo": conta.saldo
            }
            lista_contas.append(info_conta)

        return lista_contas