import datetime
import re

class Cliente:
    contador_id=1     # Contador global da classe "Cliente" que será associado à cada novo cliente
    def __init__(self,nome,cpf,data_nascimento,email,endereco,telefone, senha):
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
        data_atual = datetime.datetime.now()  # Captura da data e hora associada à criação do cliente
        self.data_cadastro = data_atual.strftime("%Y-%m-%d %H:%M:%S")  # Formatação da data e hora

    

    def validar_email(self, email):           # Valida se o email apresenta o padrao esperado
        if not self.verificar_email(email):
            print(f"Erro: E-mail {email} inválido")
            return None
        return email
    
    def criar_senha(self,senha_criada):  # Verifica se a senha atende aos requisitos necessarios para sua criacao
        if len(senha_criada)<9:
            return False
        tem_num=False              # variavel auxiliar para verificar a presença de numero na senha
        tem_letra=False            # variavel auxiliar para verificar a presença de letra na senha
        tem_caractere=False        # variavel auxiliar para verificar a presença de caractere especial na senha
        caracteres_especiais = r"!@#$%^&*(),.?/:{~}[]<>"

        for i in senha_criada:     # percorre a senha em busca de um numero
            if i.isdigit():        # verifica a presença de ao menos um numero     
                tem_num=True 
            elif i.isalpha():      # verifica a presença de ao menos uma letra
                tem_letra=True
            elif i in caracteres_especiais:   # verifica a presença de ao menos um caractere especial
                tem_caractere=True
        return (tem_num and tem_letra and tem_caractere) # retorna "True" caso a senha atenda aos requisitos necessários

    def verificar_senha(self,senha_inserida): # Autenticaçao para verificar se a senha inserida pelo cliente é a sua senha
        if self.senha==senha_inserida:
            return True
        return False
    
    def verificar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))


    
    def atualizar_dados(self, campo, dado_atualizado):   # Função que permite atualizar os dados do cliente
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
    
    def adicionar_conta(self, conta):       # Atrela uma nova conta ao seu respectivo cliente 
        self.contas.append(conta)
        return {"sucesso": True, "mensagem": f"Conta {conta.numero_conta} adicionada ao cliente {self.nome}."}

    
    def remover_conta(self, numero_conta):  # Remove uma conta da listas de conta de um determinado cliente
        for i in range(len(self.contas)):
            if self.contas[i].numero == numero_conta:
                conta_removida = self.contas.pop(i)
                return {"sucesso": True, "mensagem": f"Conta {numero_conta} removida do cliente {self.nome}."}
        return {"sucesso": False, "mensagem": f"Conta {numero_conta} não encontrada."}

    
    def buscar_conta(self, numero_conta):  # Encontra uma determinada conta a partir do número associado a ela
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta
        return None
    
    def listar_contas(self):               # Lista as contas de um determinado cliente
        if len(self.contas) == 0:
            return {"sucesso": True, "mensagem": f"Cliente {self.nome} não possui contas.", "contas": []}
        print(f"Contas do cliente {self.nome}:")
        lista_contas = []
        for conta in self.contas:
            print(f"- Conta {conta.numero}, Tipo: {conta.tipo}, Saldo: R$ {conta.saldo:.2f}")
            info_conta = {
                "numero": conta.numero,
                "tipo": conta.tipo,
                "saldo": conta.saldo
            }
            lista_contas.append(info_conta)
        return lista_contas