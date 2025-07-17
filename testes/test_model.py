import unittest
from unittest.mock import patch, MagicMock 
from datetime import datetime


from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica
from model.cliente import Cliente
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from model.exceptions import ContaInativaError # não diretamente testado em Cliente, mas é uma dependência de Conta

# Constantes que podem ser usadas nos testes
from utils.constantes import TAXA_MANUTENCAO_CCORRENTE, RENDIMENTO_MENSAL_CPOUPANCA,LIMITE_TRANSFERENCIA_CCORRENTE,LIMITE_TRANSFERENCIA_CPOUPANCA




class TestPessoa(unittest.TestCase):
    def setUp(self):
        """
        ***************************************** Setup dos Testes *************************************************************
        O setUp prepara o ambiente para cada teste da classe e foi utilizado ao longo da maioria da classes de testes do grupo

        Aqui, ele cria instâncias de objetos necessários, como PessoaFisica e Cliente, e inicializa atributos comuns 
        para evitar repetição de código em cada teste.
        ********************************************************************************************************
        """
        # Inicia o patch da API de CEP (vale para todos os testes)
        self.patcher = patch(
            'utils.api.API.buscar_endereco_por_cep', 
            return_value="Rua Teste, 123 - Bairro Legal, Cidade Ficticia - UF, 12345-678"
        )
        self.mock_buscar_endereco = self.patcher.start()

        self.nome_pf = "Joao Silva"
        self.email_pf = "joao@email.com"
        self.cpf = "12345678900"
        self.cep = "12345678"
        self.num_endereco = "100"
        self.telefone_pf = "31999998888"
        self.data_nasc_str = "01/01/1990"
        self.data_nasc_dt = datetime(1990, 1, 1)
        self.endereco_mock = "Rua Mockada, 100 - Bairro Mock, Cidade Mock - MC, 12345678"

        self.pessoa_fisica = PessoaFisica(
            nome=self.nome_pf,
            email=self.email_pf,
            numero_documento=self.cpf,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco=self.endereco_mock,
            telefone=self.telefone_pf,
            data_nascimento=self.data_nasc_str
        )

        self.nome_pj = "Empresa XYZ"
        self.email_pj = "contato@xyz.com"
        self.cnpj = "12345678000199"
        self.telefone_pj = "3133334444"
        self.nome_fantasia = "XYZ Solucoes"

        self.pessoa_juridica = PessoaJuridica(
            nome=self.nome_pj,
            email=self.email_pj,
            numero_documento=self.cnpj,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco=self.endereco_mock,
            telefone=self.telefone_pj,
            nome_fantasia=self.nome_fantasia
        )

    def tearDown(self):
        # Para o patch da API de CEP após cada teste
        self.patcher.stop()

    def test_pessoa_fisica_criacao(self):
        """
        /************************ Teste 1 ****************************
        Verifica criação de PessoaFisica com todos os atributos básicos.

        Teste para garantir o armazenamento correto dos dados iniciais.
        ****************************************************************/
        """
        self.assertEqual(self.pessoa_fisica.get_nome(), self.nome_pf)
        self.assertEqual(self.pessoa_fisica.get_email(), self.email_pf)
        self.assertEqual(self.pessoa_fisica.get_numero_documento(), self.cpf)
        self.assertEqual(self.pessoa_fisica.get_data_nascimento(), self.data_nasc_dt)
        self.assertEqual(self.pessoa_fisica.get_tipo(), "fisica")
        self.assertEqual(self.pessoa_fisica.get_endereco(), "Rua Teste, 123 - Bairro Legal, Cidade Ficticia - UF, 12345-678")
        self.mock_buscar_endereco.assert_called_with(self.cep, self.num_endereco)

    def test_pessoa_fisica_str(self):
        """
        /************************ Teste 2 ****************************
        Verifica método __str__ de PessoaFisica.

        Importante para fins de exibição. 
        ****************************************************************/
        """
        self.assertEqual(str(self.pessoa_fisica), f"{self.nome_pf} (CPF: {self.cpf})")

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_fisica_instanciacao_com_data_nascimento_datetime(self, mock_api):
        """
        /************************ Teste 3 ****************************
        Verifica criação de PessoaFisica aceitando datetime para data de nascimento.

        Permite verificar se a classe aceita data_nascimento tanto em formato string quanto datetime.
        ****************************************************************/
        """
        pf = PessoaFisica(
            nome="Maria",
            email="m@m.com",
            numero_documento="98765432100",
            cep="87654321",
            numero_endereco="200",
            endereco="End Ficticio",
            telefone="31988887777",
            data_nascimento=datetime(1995, 5, 5)
        )
        self.assertEqual(pf.get_data_nascimento(), datetime(1995, 5, 5))

    def test_pessoa_juridica_criacao(self):
        """
        /************************ Teste 4 ****************************
        Verifica criação de PessoaJuridica com atributos básicos e nome fantasia.

        Teste para assegurar diferenciação entre pessoas físicas e jurídicas.
        ****************************************************************/
        """
        self.assertEqual(self.pessoa_juridica.get_nome(), self.nome_pj)
        self.assertEqual(self.pessoa_juridica.get_email(), self.email_pj)
        self.assertEqual(self.pessoa_juridica.get_numero_documento(), self.cnpj)
        self.assertEqual(self.pessoa_juridica.get_nome_fantasia(), self.nome_fantasia)
        self.assertEqual(self.pessoa_juridica.get_tipo(), "juridica")

    def test_pessoa_juridica_str(self):
        """
        /************************ Teste 5 ****************************
        Verifica método __str__ de PessoaJuridica.

        Teste para verificar a exibição clara de detalhes de empresas.
        ****************************************************************/
        """
        self.assertEqual(str(self.pessoa_juridica), f"{self.nome_fantasia} (CNPJ: {self.cnpj})")

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_juridica_sem_nome_fantasia(self, mock_api):
        """
        /************************ Teste 6 ****************************
        Verifica comportamento sem nome fantasia fornecido.

        Verifica se a ausência do nome fantasia é tratada corretamente como campo opcional
        ****************************************************************/
        """
        pj_sem_fantasia = PessoaJuridica(
            nome=self.nome_pj,
            email=self.email_pj,
            numero_documento=self.cnpj,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco="End Ficticio",
            telefone=self.telefone_pj
        )
        self.assertEqual(pj_sem_fantasia.get_nome_fantasia(), "")
        self.assertEqual(
            str(pj_sem_fantasia),
            f"Empresa sem nome fantasia (CNPJ: {self.cnpj})"
        )

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_fisica_cpf_invalido_gera_erro(self, mock_api):
        """
        /************************ Teste 7 ****************************
        Verifica que CPF inválido gera ValueError na criação de PessoaFisica.

        Esse teste é importante para validação de dados sensíveis e segurança.
        ****************************************************************/
        """
        with self.assertRaises(ValueError):
            PessoaFisica(
                nome="Nome Valido",
                email="email@valido.com",
                numero_documento="123",
                cep="12345678",
                numero_endereco="10",
                endereco="Rua X",
                telefone="31912345678",
                data_nascimento="01/01/2000"
            )

# --- Testes para Cliente
class TestCliente(unittest.TestCase):

    # Mock para a API de busca de endereço que é chamada no construtor de Pessoa
    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua Teste, 100 - Bairro Mock, Cidade Mock - MC, 12345-678")
    def setUp(self, mock_buscar_endereco_api):
        # Criando uma instância REAL de PessoaFisica
        self.dados_pessoa_fisica = {
            "nome": "Usuario Teste",
            "email": "usuario@teste.com",
            "numero_documento": "11122233344",
            "cep": "30100100",
            "numero_endereco": "100",
            "endereco": "Rua dos Testes, 100", 
            "telefone": "31912345678",
            "data_nascimento": "01/01/1990"
        }
        self.pessoa_real = PessoaFisica(**self.dados_pessoa_fisica)

        self.senha_correta = "Senha@Forte123"
        self.cliente = Cliente(pessoa=self.pessoa_real, senha=self.senha_correta)
        self.mock_buscar_endereco_api = mock_buscar_endereco_api 

    def test_cliente_criacao(self):
        """
        /************************ Teste 1 ****************************
         Testa a criação de um Cliente e a associação correta com uma Pessoa.
        *************************************************************/"""
        self.assertEqual(self.cliente.pessoa, self.pessoa_real)
        self.assertEqual(self.cliente.numero_documento, self.dados_pessoa_fisica["numero_documento"])
        self.assertTrue(self.cliente.verificar_senha(self.senha_correta))
    
        self.mock_buscar_endereco_api.assert_called_once_with(
            self.dados_pessoa_fisica["cep"], self.dados_pessoa_fisica["numero_endereco"]
        )


    def test_cliente_verificar_senha_incorreta(self):
        """
        /************************ Teste 2 ****************************
        Testa a verificação de senha com valor incorreto.
        
        Importante para a segurança do sistema, impedindo acessos indevidos.
        *************************************************************/"""
        self.assertFalse(self.cliente.verificar_senha("senhaErrada123"))

    def test_cliente_alterar_senha_sucesso(self):
        """
        /************************ Teste 3 ****************************
        Testa a alteração de senha com sucesso.

        Garante que o usuário consiga mudar sua senha de forma segura
        *************************************************************/
        """
        nova_senha = "NovaSenha@456"
        with patch('utils.validadores.validar_cliente.ValidarCliente.senha') as mock_validar_senha:
            self.cliente.alterar_senha(self.senha_correta, nova_senha)
            mock_validar_senha.assert_called_once_with(nova_senha) 
            self.assertTrue(self.cliente.verificar_senha(nova_senha))

    def test_cliente_alterar_senha_atual_incorreta(self):
        """
        /************************ Teste 4 ****************************
        Testa se o erro é levantado ao tentar alterar a senha com a senha atual errada.

        Permite testar se funciona o impedimento que uma senha seja trocada por alguém sem autenticação correta.
        *************************************************************/
        """
        with self.assertRaisesRegex(ValueError, "Senha atual incorreta."):
            self.cliente.alterar_senha("senhaAtualErrada", "NovaSenha@456")

    @patch('utils.validadores.validar_cliente.ValidarCliente.senha', side_effect=ValueError("Nova senha eh fraca"))
    def test_cliente_alterar_senha_nova_invalida(self, mock_validar_senha_com_erro):
        """
        /************************ Teste 5 ****************************
        Testa se erro é levantado ao tentar alterar a senha para uma senha nova inválida.
        *************************************************************/
        """
        with self.assertRaisesRegex(ValueError, "Nova senha eh fraca"):
            self.cliente.alterar_senha(self.senha_correta, "fraca123")
        mock_validar_senha_com_erro.assert_called_once_with("fraca123")


    def test_cliente_possui_conta(self):
        """
        /************************ Teste 6 ****************************
        Testa se o método possui_conta retorna True apenas quando o cliente realmente tem contas.

        Teste que permite ver o controle de cadastro e para a lógica da interface.
        *************************************************************/
        """
        self.assertFalse(self.cliente.possui_conta()) # 

        with patch('utils.validadores.validar_conta.ValidarConta.todos_campos', return_value=[]) as mock_validar_todos_campos_conta:
            conta_real_para_teste = ContaCorrente(numero="9999")
        self.cliente.contas = [conta_real_para_teste] 
        self.assertTrue(self.cliente.possui_conta())


    def test_cliente_criacao_tipo_pessoa_invalido(self):
        """
        /************************ Teste 7 ****************************
        Testa se TypeError é levantado quando o parâmetro 'pessoa' não é do tipo esperado.
        *************************************************************/
        """

        with self.assertRaisesRegex(TypeError, "O parâmetro 'pessoa' deve ser um objeto da classe Pessoa."):
            Cliente(pessoa="nao_eh_pessoa_obj", senha="123")

    def test_cliente_criacao_tipo_conta_invalido(self):
        """
        /************************ Teste 8 ****************************
        Testa se TypeError é levantado quando algum item em 'contas' não é do tipo Conta.

        Importante para garantir integridade dos dados.
         *************************************************************/
        """

        with patch('utils.validadores.validar_conta.ValidarConta.todos_campos', return_value=[]):
            conta_valida_real = ContaCorrente(numero="8888")

        with self.assertRaisesRegex(TypeError, "Todos os itens em 'contas' devem ser objetos da classe Conta."):
            Cliente(pessoa=self.pessoa_real, senha="123", contas=[conta_valida_real, "nao_eh_conta_obj"])

# --- Testes para ContaCorrente e ContaPoupanca ---
class TestContasBancarias(unittest.TestCase):

    def setUp(self):
        """
        /************************ Setup Testes de Contas ****************************
        Prepara instâncias de ContaCorrente e ContaPoupanca com dados válidos,
        além de contas de destino para operações de transferência.
        Essencial para inicializar objetos comuns e evitar repetição de código.
        ***************************************************************************
        """
        self.conta_corrente = ContaCorrente(numero="1001") 
        self.conta_poupanca = ContaPoupanca(numero="2002", saldo=1000.0)

        
        self.conta_destino_cc = ContaCorrente(numero="1003", saldo=500.0)
        self.conta_destino_cp = ContaPoupanca(numero="2004", saldo=200.0)


    
    def test_conta_corrente_criacao(self):
        """
        /************************ Teste 1 ****************************
        Testa a criação de uma ContaCorrente com valores padrão.

        Para verificar que atributos como número de conta, saldo inicial,
        estado e histórico estão sendo corretamente inicializados.
        ****************************************************************/
        """
        self.assertEqual(self.conta_corrente.get_numero_conta(), "1001") 
        self.assertEqual(self.conta_corrente.get_saldo(), 0.0) 
        self.assertTrue(self.conta_corrente.get_estado_da_conta()) 
        self.assertIsInstance(self.conta_corrente.get_historico(), list)
        self.assertEqual(self.conta_corrente.limite_transferencia, LIMITE_TRANSFERENCIA_CCORRENTE) 

    def test_conta_corrente_atualizacao_mensal(self):
        """
        /************************ Teste 2 ****************************
        Testa a taxa de manutenção na atualização mensal da ContaCorrente.

        Permite validar se a tarifa é debitada e registrada no histórico.
        ****************************************************************/
        """
        saldo_inicial = 200.0
        cc = ContaCorrente("1111", saldo=saldo_inicial)
        cc.atualizacao_mensal() # [cite: 190]
        self.assertEqual(cc.get_saldo(), saldo_inicial - TAXA_MANUTENCAO_CCORRENTE)
        self.assertIn(f"taxa de manutenção de R$ {TAXA_MANUTENCAO_CCORRENTE:.2f} cobrada", cc.get_historico()[-1])

    def test_conta_corrente_atualizacao_mensal_conta_inativa(self):
        """
        /************************ Teste 3 ****************************
        Testa se ContaInativaError é levantado ao tentar atualizar conta inativa.

        Para testar se operações não estão sendo permitidas em contas fechadas.
        ****************************************************************/
        """
        cc = ContaCorrente("1112", saldo=100.0, ativa=False)
        with self.assertRaises(ContaInativaError):
            cc.atualizacao_mensal()

    # Testes para ContaPoupanca
    def test_conta_poupanca_criacao(self):
        """
        /************************ Teste 4 ****************************
        Testa a criação de uma ContaPoupanca com saldo inicial.
        ****************************************************************/
        """
        self.assertEqual(self.conta_poupanca.get_numero_conta(), "2002")
        self.assertEqual(self.conta_poupanca.get_saldo(), 1000.0)
        self.assertEqual(self.conta_poupanca.limite_transferencia, LIMITE_TRANSFERENCIA_CPOUPANCA) 

    def test_conta_poupanca_atualizacao_mensal(self):
        """
        /************************ Teste 5 ****************************
        Testa o rendimento na atualização mensal da ContaPoupanca.

        Essencial para validar que o juros mensal é aplicado e registrado no histórico.
        ****************************************************************/
        """
        saldo_inicial = self.conta_poupanca.get_saldo()
        rendimento_esperado = saldo_inicial * RENDIMENTO_MENSAL_CPOUPANCA
        self.conta_poupanca.atualizacao_mensal() # [cite: 196]
        self.assertEqual(self.conta_poupanca.get_saldo(), saldo_inicial + rendimento_esperado)
        self.assertIn(f"rendimento de R$ {rendimento_esperado:.2f} aplicado", self.conta_poupanca.get_historico()[-1])

    def test_conta_poupanca_atualizacao_mensal_conta_inativa(self):
        """
        /************************ Teste 6 ****************************
        Testa se ContaInativaError é levantado ao atualizar ContaPoupanca inativa.

        Permite testar o impedimento de operações em contas encerradas.
        ****************************************************************/
        """
        cp = ContaPoupanca("2223", saldo=100.0, ativa=False)
        with self.assertRaises(ContaInativaError):
            cp.atualizacao_mensal()

    def test_conta_transferir_sucesso(self):
        """
        /************************ Teste 7 ****************************
        Testa uma transferência bem-sucedida entre contas.

        Permite testar operações de histórico corretos.
        ****************************************************************/
        """
        remetente = ContaCorrente("3001", saldo=100.0)
        destinatario = ContaPoupanca("4001", saldo=50.0)
        valor_transferencia = 30.0

        remetente.transferir(destinatario, valor_transferencia) 

        self.assertEqual(remetente.get_saldo(), 100.0 - valor_transferencia)
        self.assertEqual(destinatario.get_saldo(), 50.0 + valor_transferencia)
        self.assertIn(f"Transferência de R$ {valor_transferencia:.2f} para conta {destinatario.get_numero_conta()}", remetente.get_historico()[-1])
        self.assertIn(f"Recebido R$ {valor_transferencia:.2f} da conta {remetente.get_numero_conta()}", destinatario.get_historico()[-1])

    def test_conta_transferir_conta_origem_inativa(self):
        """
        /************************ Teste 8 ****************************
        Testa transferência de conta de origem inativa.

        Testar que contas encerradas realmente não conseguem transferir.
        ****************************************************************/
        """
        remetente = ContaCorrente("3002", saldo=100.0, ativa=False)
        destinatario = ContaPoupanca("4002", saldo=50.0)
        with self.assertRaisesRegex(ContaInativaError, f"A conta {remetente.get_numero_conta()} está inativa"): 
            remetente.transferir(destinatario, 50.0)

    def test_conta_transferir_conta_destino_inativa(self):
        """
        /************************ Teste 9 ****************************
        Testa transferência para conta de destino inativa.

        Novamente um teste para impedir operações (recebimento) com contas encerradas.
        ****************************************************************/
        """
        remetente = ContaCorrente("3003", saldo=100.0)
        destinatario = ContaPoupanca("4003", saldo=50.0, ativa=False)
        with self.assertRaisesRegex(ContaInativaError, f"A conta {destinatario.get_numero_conta()} está inativa"): 
            remetente.transferir(destinatario, 50.0)

    def test_conta_transferir_valor_negativo(self):
        """
        /************************ Teste 10 ***************************
        Testa transferência com valor negativo.

        Teste o entrave de uma tarefa simples, mas básica para o correto funcionamento do sistema do nosso grupo.
        ****************************************************************/
        """
        remetente = ContaCorrente("3004", saldo=100.0)
        destinatario = ContaPoupanca("4004", saldo=50.0)
        with self.assertRaisesRegex(ValueError, "O valor da transferência deve ser positivo."): 
            remetente.transferir(destinatario, -50.0)

    def test_conta_transferir_saldo_insuficiente(self):
        """
        /************************ Teste 11 ***************************
        Testa transferência com saldo insuficiente.

        Seguindo a mesma lógica do anterior, mas aqui, testa o impedimento de débitos que resultariam em saldo negativo.
        ****************************************************************/
        """
        remetente = ContaCorrente("3005", saldo=50.0)
        destinatario = ContaPoupanca("4005", saldo=50.0)
        with self.assertRaisesRegex(ValueError, "Saldo insuficiente para a transferência."): # [cite: 169]
            remetente.transferir(destinatario, 100.0)

    def test_conta_transferir_acima_limite(self):
        """
        /************************ Teste 12 ***************************
        Testa transferência acima do limite permitido pela conta de origem.

        Essencial para garantir respeito às regras de limite de transferência e validar
        o funcionamento correto da ideia de constantes definida pelao nosso grupo.
        ****************************************************************/
        """
        remetente = ContaPoupanca("3006", saldo=LIMITE_TRANSFERENCIA_CPOUPANCA + 100) # Saldo suficiente
        destinatario = ContaCorrente("4006", saldo=50.0)
        valor_acima_limite = LIMITE_TRANSFERENCIA_CPOUPANCA + 1.0
        with self.assertRaisesRegex(ValueError, f"O valor da transferência excede o limite de R\\$ {remetente.limite_transferencia:.2f}."): # [cite: 169, 195]
            remetente.transferir(destinatario, valor_acima_limite)

    def test_conta_encerrar_conta(self):
        """
        /************************ Teste 13 ***************************
        Testa o encerramento de uma conta.

        Importante para validar se o estado é alterado e registrado no histórico.
        ****************************************************************/
        """
        conta_para_encerrar = ContaCorrente("5001", saldo=10.0)
        self.assertTrue(conta_para_encerrar.get_estado_da_conta())
        conta_para_encerrar.encerrar_conta() 
        self.assertFalse(conta_para_encerrar.get_estado_da_conta())
        self.assertIn("Conta encerrada", conta_para_encerrar.get_historico()[-1])

    def test_conta_str(self):
        """
        /************************ Teste 14 ***************************
        Testa a representação em string de uma conta.

        Essencial para exibição legível de número de conta e saldo.
        ****************************************************************/
        """
        cc = ContaCorrente("6001", saldo=123.45)
        self.assertIn("Conta 6001", str(cc)) 
        self.assertIn("Saldo: R$ 123.45", str(cc)) 
        
    def test_conta_instanciacao_com_dados_invalidos(self):
        """
        /************************ Teste 15 ***************************
        Testa se ValueError é levantado com dados inválidos na criação da conta.

        Permite verificar a validação de formato de número de conta.
        ****************************************************************/
        """
        
        with self.assertRaises(ValueError) as cm:
            ContaCorrente(numero="12", saldo=100.0) 
        self.assertIn("Número da conta muito curto", str(cm.exception))
       








