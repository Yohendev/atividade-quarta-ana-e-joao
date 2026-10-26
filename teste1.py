import unittest
import os
from io import StringIO
import sys

class GerenciadorPedidos:
    def _init_(self):
        self.itens = []
        self.estoque = {}
        self.historico = []
        self.total_vendido = 0
        self.estoque["CANETA"] = 100
        self.estoque["CADERNO"] = 50
        self.estoque["MOCHILA"] = 10
        self.estoque["CALCULADORA"] = 5

    def adicionar_item(self, produto, qtd, preco):
        self.itens.append([produto, str(qtd), str(preco)])

    def processar_pedido(self, nome, email, tipo_cliente, pagamento, parcelas,
                         rua, numero, cidade, uf, cep):
        if nome is None or nome.strip() == "":
            return "ERRO: cliente sem nome"
        if email is None or "@" not in email or "." not in email:
            return "ERRO: email invalido"
        if len(self.itens) == 0:
            return "ERRO: pedido vazio"
        if cep is None or len(cep.replace("-", "")) != 8:
            return "ERRO: cep invalido"
        for item in self.itens:
            if item[0] not in self.estoque:
                return "ERRO: produto inexistente " + item[0]
            if self.estoque[item[0]] < int(item[1]):
                return "ERRO: estoque insuficiente " + item[0]

        subtotal = 0
        for item in self.itens:
            subtotal += int(item[1]) * float(item[2])

        desconto = 0
        if tipo_cliente == "COMUM":
            if subtotal > 500:
                desconto = subtotal * 0.05
        elif tipo_cliente == "VIP":
            if subtotal > 500:
                desconto = subtotal * 0.15
            else:
                desconto = subtotal * 0.10
        elif tipo_cliente == "FUNCIONARIO":
            desconto = subtotal * 0.20
        else:
            return "ERRO: tipo de cliente desconhecido"

        frete = 0
        if uf == "PE":
            frete = 12.5
        elif (uf == "PB" or uf == "AL" or uf == "RN" or uf == "BA"
              or uf == "SE" or uf == "CE" or uf == "PI" or uf == "MA"):
            frete = 22.9
        else:
            frete = 39.9
        if subtotal - desconto > 300 or tipo_cliente == "VIP":
            frete = 0

        total = subtotal - desconto + frete
        if pagamento == "PIX":
            total = total * 0.95
        elif pagamento == "BOLETO":
            total = total + 2.5
        elif pagamento == "CARTAO":
            if parcelas < 1 or parcelas > 12:
                return "ERRO: parcelas invalidas"
            if parcelas > 3:
                total = total * (1 + 0.0199 * parcelas)
        else:
            return "ERRO: forma de pagamento invalida"
        total = round(total * 100.0) / 100.0

        for item in self.itens:
            self.estoque[item[0]] = self.estoque[item[0]] - int(item[1])

        endereco = rua + ", " + numero + ", " + cidade + "/" + uf + ", CEP " + cep

        try:
            f = open("pedidos.csv", "a", encoding="utf-8")
            f.write(nome + ";" + email + ";" + tipo_cliente + ";" + pagamento + ";"
                    + str(total) + ";" + endereco + "\n")
            f.close()
        except OSError as e:
            print("Falha ao salvar pedido: " + str(e))

        mensagem = "Ola " + nome + ", seu pedido foi confirmado. "
        if tipo_cliente == "VIP":
            mensagem += "Obrigado por ser VIP! Frete gratis garantido. "
        elif tipo_cliente == "FUNCIONARIO":
            mensagem += "Desconto de colaborador aplicado. "
        mensagem += "Total: R$ " + "%.2f" % total + ". Entrega em: " + endereco
        print("[EMAIL para " + email + "] " + mensagem)

        self.historico.append(nome + "|" + tipo_cliente + "|" + str(total))
        self.total_vendido += total
        self.itens.clear()
        return "OK: " + "%.2f" % total

    def calcular_orcamento(self, tipo_cliente, uf):
        subtotal = 0
        for item in self.itens:
            subtotal += int(item[1]) * float(item[2])
        desconto = 0
        if tipo_cliente == "COMUM":
            if subtotal > 500:
                desconto = subtotal * 0.05
        elif tipo_cliente == "VIP":
            if subtotal > 500:
                desconto = subtotal * 0.15
            else:
                desconto = subtotal * 0.10
        elif tipo_cliente == "FUNCIONARIO":
            desconto = subtotal * 0.2
        frete = 0
        if uf == "PE":
            frete = 12.5
        elif (uf == "PB" or uf == "AL" or uf == "RN" or uf == "BA"
              or uf == "SE" or uf == "CE" or uf == "PI"):
            frete = 22.9
        else:
            frete = 39.9
        if subtotal - desconto > 300 or tipo_cliente == "VIP":
            frete = 0
        return round((subtotal - desconto + frete) * 100.0) / 100.0

    def criar_relatorio(self):
        r = "=== RELATORIO DE VENDAS ===\n"
        vip = 0
        comum = 0
        func = 0
        for h in self.historico:
            partes = h.split("|")
            if partes[1] == "VIP":
                vip += 1
            elif partes[1] == "COMUM":
                comum += 1
            elif partes[1] == "FUNCIONARIO":
                func += 1
            r += partes[0] + " (" + partes[1] + "): R$ " + "%.2f" % float(partes[2]) + "\n"
        r += "Pedidos VIP: " + str(vip) + "\n"
        r += "Pedidos COMUM: " + str(comum) + "\n"
        r += "Pedidos FUNCIONARIO: " + str(func) + "\n"
        r += "Total vendido: R$ " + "%.2f" % self.total_vendido + "\n"
        if self.total_vendido > 10000:
            r += "Meta mensal atingida!\n"
        return r

    def verificar_estoque(self):
        alerta = ""
        for produto in self.estoque:
            if self.estoque[produto] < 5:
                alerta += ("ALERTA: " + produto + " com estoque baixo ("
                           + str(self.estoque[produto]) + ")\n")
                print("[EMAIL para compras@loja.com] Repor " + produto)
        return alerta

    def mensagem_promocional(self, tipo_cliente):
        if tipo_cliente == "VIP":
            return "Ofertas exclusivas: 15% em compras acima de R$ 500!"
        elif tipo_cliente == "COMUM":
            return "Compre acima de R$ 500 e ganhe 5% de desconto!"
        elif tipo_cliente == "FUNCIONARIO":
            return "Lembrete: seu desconto de 20% vale em toda a loja."
        else:
            return ""


class TestCaracterizacaoGerenciadorPedidos(unittest.TestCase):
    def setUp(self):
        self.gp = GerenciadorPedidos()
        if os.path.exists("pedidos.csv"):
            os.remove("pedidos.csv")
            
        self.held_stdout = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

    def tearDown(self):
        sys.stdout = self.original_stdout
        if os.path.exists("pedidos.csv"):
            os.remove("pedidos.csv")

    def test_erro_cliente_sem_nome(self):
        res = self.gp.processar_pedido("   ", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: cliente sem nome")

    def test_erro_email_invalido(self):
        res = self.gp.processar_pedido("Joao", "email_sem_arroba.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: email invalido")

    def test_erro_pedido_vazio(self):
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: pedido vazio")

    def test_erro_cep_invalido(self):
        self.gp.adicionar_item("CANETA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "1234567")
        self.assertEqual(res, "ERRO: cep invalido")

    def test_erro_produto_inexistente(self):
        self.gp.adicionar_item("MESA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: produto inexistente MESA")

    def test_erro_estoque_insuficiente(self):
        self.gp.adicionar_item("MOCHILA", 15, 50.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Cid", "PE", "12345678")
        self.assertEqual(res, "ERRO: estoque insuficiente MOCHILA")

    def test_sucesso_cliente_comum_sem_desconto_frete_pe_pix(self):
        self.gp.adicionar_item("CANETA", 10, 5.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "PIX", 1, "Rua", "1", "Recife", "PE", "12345678")
        self.assertEqual(res, "OK: 59.38")
        self.assertEqual(self.gp.estoque["CANETA"], 90)
        self.assertTrue(os.path.exists("pedidos.csv"))

    def test_sucesso_cliente_comum_com_desconto_frete_nordeste_boleto(self):
        self.gp.adicionar_item("CADERNO", 12, 50.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "BOLETO", 1, "Rua", "1", "Salvador", "BA", "12345678")
        self.assertEqual(res, "OK: 572.50")

    def test_sucesso_cliente_vip_com_desconto_maior_cartao_parcelado(self):
        self.gp.adicionar_item("CADERNO", 12, 50.0) 
        res = self.gp.processar_pedido("Joao", "a@b.com", "VIP", "CARTAO", 4, "Rua", "1", "SP", "SP", "12345678")
        self.assertEqual(res, "OK: 550.60")

    def test_sucesso_cliente_funcionario_cartao_sem_juros(self):
        self.gp.adicionar_item("MOCHILA", 1, 100.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "FUNCIONARIO", "CARTAO", 3, "Rua", "1", "RJ", "RJ", "12345678")
        self.assertEqual(res, "OK: 119.90")

    def test_erro_tipo_cliente_desconhecido(self):
        self.gp.adicionar_item("CANETA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "ALIEN", "PIX", 1, "R", "1", "C", "PE", "12345678")
        self.assertEqual(res, "ERRO: tipo de cliente desconhecido")

    def test_erro_pagamento_invalido(self):
        self.gp.adicionar_item("CANETA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "CHEQUE", 1, "R", "1", "C", "PE", "12345678")
        self.assertEqual(res, "ERRO: forma de pagamento invalida")

    def test_erro_parcelas_invalidas(self):
        self.gp.adicionar_item("CANETA", 1, 5.0)
        res = self.gp.processar_pedido("Joao", "a@b.com", "COMUM", "CARTAO", 13, "R", "1", "C", "PE", "12345678")
        self.assertEqual(res, "ERRO: parcelas invalidas")

    def test_calcular_orcamento(self):
        self.gp.adicionar_item("CANETA", 10, 5.0) 
        orcamento = self.gp.calcular_orcamento("COMUM", "PE")
        self.assertEqual(orcamento, 62.5)

    def test_verificar_estoque(self):
        self.gp.estoque["CALCULADORA"] = 2
        alerta = self.gp.verificar_estoque()
        self.assertIn("ALERTA: CALCULADORA com estoque baixo (2)", alerta)
        self.assertIn("[EMAIL para compras@loja.com] Repor CALCULADORA", self.held_stdout.getvalue())

    def test_criar_relatorio(self):
        self.gp.adicionar_item("CANETA", 10, 5.0)
        self.gp.processar_pedido("Joao", "a@b.com", "VIP", "PIX", 1, "R", "1", "C", "PE", "12345678")
        relatorio = self.gp.criar_relatorio() 
        self.assertIn("=== RELATORIO DE VENDAS ===", relatorio)
        self.assertIn("VIP", relatorio)
        self.assertIn("Pedidos VIP: 1", relatorio)
        self.assertIn("Total vendido", relatorio)

    def test_mensagem_promocional(self):
        self.assertEqual(self.gp.mensagem_promocional("VIP"), "Ofertas exclusivas: 15% em compras acima de R$ 500!")
        self.assertEqual(self.gp.mensagem_promocional("INEXISTENTE"), "")

if _name_ == "_main_":
    unittest.main()
