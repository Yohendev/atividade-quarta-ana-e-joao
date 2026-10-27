<<<<<<< HEAD
class ItemPedido:
    def __init__(self, produto, quantidade, preco):
        self.produto = produto
        self.quantidade = int(quantidade)
        self.preco = float(preco)
    def calcular_subtotal(self):
        return self.quantidade * self.preco

class Cliente:
    def __init__(self, nome, email, tipo):
        self.nome = nome; self.email = email; self.tipo = tipo
    def is_valido(self):
        if self.nome is None or self.nome.strip() == "": return "ERRO: cliente sem nome"
        if self.email is None or "@" not in self.email or "." not in self.email: return "ERRO: email invalido"
        if self.tipo not in ["COMUM", "VIP", "FUNCIONARIO"]: return "ERRO: tipo de cliente desconhecido"
        return None

class Endereco:
    def __init__(self, rua, numero, cidade, uf, cep):
        self.rua = rua; self.numero = numero; self.cidade = cidade; self.uf = uf; self.cep = cep
    def is_valido(self):
        if self.cep is None or len(self.cep.replace("-", "")) != 8: return "ERRO: cep invalido"
        return None
    def formatar(self):
        return f"{self.rua}, {self.numero}, {self.cidade}/{self.uf}, CEP {self.cep}"

class CalculadoraPreco:
    @staticmethod
    def calcular_desconto(tipo_cliente, subtotal):
        if tipo_cliente == "COMUM" and subtotal > 500: return subtotal * 0.05
        if tipo_cliente == "VIP": return subtotal * 0.15 if subtotal > 500 else subtotal * 0.10
        if tipo_cliente == "FUNCIONARIO": return subtotal * 0.20
        return 0

    @staticmethod
    def calcular_frete(uf, total_com_desconto, tipo_cliente):
        if total_com_desconto > 300 or tipo_cliente == "VIP": return 0
        if uf == "PE": return 12.5
        if uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI", "MA"]: return 22.9
        return 39.9

    @staticmethod
    def aplicar_taxas_pagamento(total, pagamento, parcelas):
        if pagamento == "PIX": return total * 0.95
        if pagamento == "BOLETO": return total + 2.5
        if pagamento == "CARTAO":
            if parcelas < 1 or parcelas > 12: raise ValueError("ERRO: parcelas invalidas")
            if parcelas > 3: return total * (1 + 0.0199 * parcelas)
        elif pagamento not in ["PIX", "BOLETO", "CARTAO"]: raise ValueError("ERRO: forma de pagamento invalida")
        return total

class RepositorioPedidosCSV:
    @staticmethod
    def salvar(linha):
        try:
            with open("pedidos.csv", "a", encoding="utf-8") as f: f.write(linha + "\n")
        except OSError as e: print("Falha ao salvar pedido: " + str(e))

class ServicoNotificacao:
    @staticmethod
    def confirmar_pedido(cliente, total, endereco):
        mensagem = f"Ola {cliente.nome}, seu pedido foi confirmado. "
        if cliente.tipo == "VIP": mensagem += "Obrigado por ser VIP! Frete gratis garantido. "
        elif cliente.tipo == "FUNCIONARIO": mensagem += "Desconto de colaborador aplicado. "
        mensagem += f"Total: R$ {total:.2f}. Entrega em: {endereco}"
        print(f"[EMAIL para {cliente.email}] {mensagem}")

class GerenciadorPedidos:
    def __init__(self):
        self.itens = []
        self.estoque = {"CANETA": 100, "CADERNO": 50, "MOCHILA": 10, "CALCULADORA": 5}
        self.historico = []
        self.total_vendido = 0

    def adicionar_item(self, produto, qtd, preco):
        self.itens.append(ItemPedido(produto, qtd, preco))

    def processar_pedido(self, nome, email, tipo_cliente, pagamento, parcelas, rua, numero, cidade, uf, cep):
        cliente = Cliente(nome, email, tipo_cliente)
        if erro_cliente := cliente.is_valido(): return erro_cliente

        endereco = Endereco(rua, numero, cidade, uf, cep)
        if erro_endereco := endereco.is_valido(): return erro_endereco

        if not self.itens: return "ERRO: pedido vazio"

        for item in self.itens:
            if item.produto not in self.estoque: return "ERRO: produto inexistente " + item.produto
            if self.estoque[item.produto] < item.quantidade: return "ERRO: estoque insuficiente " + item.produto

        subtotal = sum(item.calcular_subtotal() for item in self.itens)
        desconto = CalculadoraPreco.calcular_desconto(cliente.tipo, subtotal)
        frete = CalculadoraPreco.calcular_frete(endereco.uf, subtotal - desconto, cliente.tipo)
        total = subtotal - desconto + frete

        try:
            total = CalculadoraPreco.aplicar_taxas_pagamento(total, pagamento, parcelas)
        except ValueError as e: return str(e)
        
        total = round(total, 2)

        for item in self.itens: self.estoque[item.produto] -= item.quantidade

        end_formatado = endereco.formatar()
        linha_csv = f"{cliente.nome};{cliente.email};{cliente.tipo};{pagamento};{total};{end_formatado}"
        RepositorioPedidosCSV.salvar(linha_csv)
        ServicoNotificacao.confirmar_pedido(cliente, total, end_formatado)

        self.historico.append(f"{cliente.nome}|{cliente.tipo}|{total}")
        self.total_vendido += total
        self.itens.clear()
        
        return f"OK: {total:.2f}"
=======
class GerenciadorPedidos:

    def __init__(self):
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

    def gerar_relatorio(self):
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
>>>>>>> b741db6e12ffaa234034cde8caf7873583997293
