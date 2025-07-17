import unittest

from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from model.exceptions import ContaInativaError

# Importando constantes que podem ser usadas nos testes
from utils.constantes import TAXA_MANUTENCAO_CCORRENTE, RENDIMENTO_MENSAL_CPOUPANCA,LIMITE_TRANSFERENCIA_CCORRENTE, LIMITE_TRANSFERENCIA_CPOUPANCA


# --- Testes para ContaCorrente e ContaPoupanca ---
class TestContasBancarias(unittest.TestCase):

    def setUp(self):
        """
        /************************ Setup Testes de Contas ****************************
        O setUp prepara o ambiente para cada teste da classe e foi utilizado ao longo da maiori da snossas classes de testes.

        Aqui, ele cria instâncias de ContaCorrente e ContaPoupanca com dados válidos,
        além de contas de destino para operações de transferência.
        ***************************************************************************
        """
        self.conta_corrente = ContaCorrente(numero="1001")
        self.conta_poupanca = ContaPoupanca(numero="2002", saldo=1000.0)

        self.conta_destino_cc = ContaCorrente(numero="1003", saldo=500.0)
        self.conta_destino_cp = ContaPoupanca(numero="2004", saldo=200.0)


    # Testes para ContaCorrente
    def test_conta_corrente_criacao(self):
        """
        /************************ Teste 1 ****************************
        Testa a criação de uma ContaCorrente com valores padrão.
        
        Teste para verificar e garantir que número, saldo, estado e histórico
        sejam corretamente inicializados.
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
        Testa a aplicação da taxa de manutenção na atualização mensal.

        Teste para verificar o correto débito de tarifa e registro no histórico.
        ****************************************************************/
        """
        saldo_inicial = 200.0
        cc = ContaCorrente("1111", saldo=saldo_inicial)
        cc.atualizacao_mensal()
        self.assertEqual(cc.get_saldo(), saldo_inicial - TAXA_MANUTENCAO_CCORRENTE)
        self.assertIn(
            f"taxa de manutenção de R$ {TAXA_MANUTENCAO_CCORRENTE:.2f} cobrada",
            cc.get_historico()[-1]
        )

    def test_conta_corrente_atualizacao_mensal_conta_inativa(self):
        """
        /************************ Teste 3 ****************************
        Testa se ContaInativaError é levantado ao atualizar conta inativa.

        Teste para impedir operações em contas encerradas.
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

        Verificaçao do cálculo correto de rendimentos.
        ****************************************************************/
        """
        self.assertEqual(self.conta_poupanca.get_numero_conta(), "2002")
        self.assertEqual(self.conta_poupanca.get_saldo(), 1000.0)
        self.assertEqual(
            self.conta_poupanca.limite_transferencia,
            LIMITE_TRANSFERENCIA_CPOUPANCA
        )

    def test_conta_poupanca_atualizacao_mensal_conta_inativa(self):
        """
        /************************ Teste 6 ****************************
        Testa se ContaInativaError é levantado ao atualizar poupança inativa.

        Crucial para impedir ações em contas encerradas.
        ****************************************************************/
        """
        cp = ContaPoupanca("2223", saldo=100.0, ativa=False)
        with self.assertRaises(ContaInativaError):
            cp.atualizacao_mensal()

    # Testes comuns de Conta 
    def test_conta_transferir_sucesso(self):
        """
        /************************ Teste 7 ****************************
        Testa transferência bem-sucedida entre contas.

        Para olhar funcionamento do débito, crédito e histórico.
        ****************************************************************/
        """
        remetente = ContaCorrente("3001", saldo=100.0)
        destinatario = ContaPoupanca("4001", saldo=50.0)
        valor = 30.0

        remetente.transferir(destinatario, valor)

        self.assertEqual(remetente.get_saldo(), 100.0 - valor)
        self.assertEqual(destinatario.get_saldo(), 50.0 + valor)
        self.assertIn(
            f"Transferência de R$ {valor:.2f} para conta {destinatario.get_numero_conta()}",
            remetente.get_historico()[-1]
        )
        self.assertIn(
            f"Recebido R$ {valor:.2f} da conta {remetente.get_numero_conta()}",
            destinatario.get_historico()[-1]
        )

    def test_conta_transferir_conta_origem_inativa(self):
        """
        /************************ Teste 8 ****************************
        Testa transferência de conta de origem inativa.

        Para ver se está funcionando obloqueio em contas encerradas.
        ****************************************************************/
        """
        remetente = ContaCorrente("3002", saldo=100.0, ativa=False)
        destinatario = ContaPoupanca("4002", saldo=50.0)
        with self.assertRaisesRegex(
            ContaInativaError,
            f"A conta {remetente.get_numero_conta()} está inativa"
        ):
            remetente.transferir(destinatario, 50.0)

    def test_conta_transferir_conta_destino_inativa(self):
        """
        /************************ Teste 9 ****************************
        Testa transferência para conta de destino inativa.

        Para olhar se esta permitindo crédito em contas encerradas.
        ****************************************************************/
        """
        remetente = ContaCorrente("3003", saldo=100.0)
        destinatario = ContaPoupanca("4003", saldo=50.0, ativa=False)
        with self.assertRaisesRegex(
            ContaInativaError,
            f"A conta {destinatario.get_numero_conta()} está inativa"
        ):
            remetente.transferir(destinatario, 50.0)

    def test_conta_transferir_valor_negativo(self):
        """
        /************************ Teste 10 ***************************
        Testa transferência com valor negativo.

        Para olhar se o comportamento com valores negativos esta correto
        ****************************************************************/
        """
        remetente = ContaCorrente("3004", saldo=100.0)
        destinatario = ContaPoupanca("4004", saldo=50.0)
        with self.assertRaisesRegex(
            ValueError,
            "O valor da transferência deve ser positivo."
        ):
            remetente.transferir(destinatario, -50.0)

    def test_conta_transferir_saldo_insuficiente(self):
        """
        /************************ Teste 11 ***************************
        Testa transferência quando saldo é insuficiente.

        Importante para prevenir saldo negativo.
        ****************************************************************/
        """
        remetente = ContaCorrente("3005", saldo=50.0)
        destinatario = ContaPoupanca("4005", saldo=50.0)
        with self.assertRaisesRegex(
            ValueError,
            "Saldo insuficiente para a transferência."
        ):
            remetente.transferir(destinatario, 100.0)

    def test_conta_transferir_acima_limite(self):
        """
        /************************ Teste 12 ***************************
        Testa transferência acima do limite da conta.

        Para verificar se as regras de limite definidas pelo nosso grupo estao sendo respeitadas.
        ****************************************************************/
        """
        remetente = ContaPoupanca(
            "3006",
            saldo=LIMITE_TRANSFERENCIA_CPOUPANCA + 100
        )
        destinatario = ContaCorrente("4006", saldo=50.0)
        valor_excedido = LIMITE_TRANSFERENCIA_CPOUPANCA + 1.0
        with self.assertRaisesRegex(
            ValueError,
            f"O valor da transferência excede o limite de R\\$ {remetente.limite_transferencia:.2f}."
        ):
            remetente.transferir(destinatario, valor_excedido)

    def test_conta_encerrar_conta(self):
        """
        /************************ Teste 13 ***************************
        Testa o encerramento de uma conta.
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

        Para verificar a formataçao de número e saldo.
        ****************************************************************/
        """
        cc = ContaCorrente("6001", saldo=123.45)
        self.assertIn("Conta 6001", str(cc))
        self.assertIn("Saldo: R$ 123.45", str(cc))
        
    def test_conta_instanciacao_com_dados_invalidos(self):
        """
        /************************ Teste 15 ***************************
        Testa ValueError em criação de conta com dados inválidos.

        Para olhar o tamanho do número de conta.
        ****************************************************************/
        """
        with self.assertRaises(ValueError) as cm:
            ContaCorrente(numero="12", saldo=100.0)
        self.assertIn("Número da conta muito curto", str(cm.exception))





