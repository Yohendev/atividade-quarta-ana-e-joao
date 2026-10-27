import unittest
import os
import sys
from io import StringIO
from gerenciador_pedidos import GerenciadorPedidos

class TestCaracterizacaoGerenciadorPedidos(unittest.TestCase):
    def setUp(self):
        self.gp = GerenciadorPedidos()
        if os.path.exists("pedidos.csv"): os.remove("pedidos.csv")
        self.held_stdout = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

    def tearDown(self):
        sys.stdout = self.original_stdout
        if os.path.exists("pedidos.csv"): os.remove("pedidos.csv")

    def test_erro_cliente_sem_nome(self):
        res = self.gp.processar_pedido("   ", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: cliente sem nome")

    def test_erro_email_invalido(self):
        res = self.gp.processar_pedido("Joao", "invalido", "COMUM", "PIX", 1, "R", "1", "C", "PE", "12345678")
        self.assertEqual(res, "ERRO: email invalido")

    def test_erro_pedido_vazio(self):
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "R", "1", "C", "PE", "12345678")
        self.assertEqual(res, "ERRO: pedido vazio")

    def test_erro_cep_invalido(self):
        self.gp.adicionar_item("CANETA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "R", "1", "C", "PE", "1234567")
        self.assertEqual(res, "ERRO: cep invalido")

    def test_sucesso_cliente_comum_sem_desconto_frete_pe_pix(self):
        self.gp.adicionar_item("CANETA", 10, 5.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "R", "1", "Rec", "PE", "12345678")
        self.assertEqual(res, "OK: 59.38")

    def test_sucesso_cliente_vip_com_desconto_maior_cartao_parcelado(self):
        self.gp.adicionar_item("CADERNO", 12, 50.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "VIP", "CARTAO", 4, "R", "1", "SP", "SP", "12345678")
        self.assertEqual(res, "OK: 550.60")

if __name__ == "__main__":
    unittest.main()
