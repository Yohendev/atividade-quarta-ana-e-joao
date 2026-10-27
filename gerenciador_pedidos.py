class GerenciadorPedidos:
    def __init__(self):
        self.itens = []
        self.estoque = {"CANETA": 100, "CADERNO": 50, "MOCHILA": 10, "CALCULADORA": 5}
        self.historico = []
        self.total_vendido = 0

    def adicionar_item(self, produto, qtd, preco):
        self.itens.append([produto, str(qtd), str(preco)])

    def processar_pedido(self, nome, email, tipo_cliente, pagamento, parcelas, rua, numero, cidade, uf, cep):
        if nome is None or nome.strip() == "": return "ERRO: cliente sem nome"
        if email is None or "@" not in email or "." not in email: return "ERRO: email invalido"
        if len(self.itens) == 0: return "ERRO: pedido vazio"
        if cep is None or len(cep.replace("-", "")) != 8: return "ERRO: cep invalido"
        
        for item in self.itens:
            if item[0] not in self.estoque: return "ERRO: produto inexistente " + item[0]
            if self.estoque[item[0]] < int(item[1]): return "ERRO: estoque insuficiente " + item[0]

        subtotal = sum(int(item[1]) * float(item[2]) for item in self.itens)

        desconto = 0
        if tipo_cliente == "COMUM":
            if subtotal > 500: desconto = subtotal * 0.05
        elif tipo_cliente == "VIP":
            if subtotal > 500: desconto = subtotal * 0.15
            else: desconto = subtotal * 0.10
        elif tipo_cliente == "FUNCIONARIO":
            desconto = subtotal * 0.20
        else:
            return "ERRO: tipo de cliente desconhecido"

        frete = 0
        if uf == "PE": frete = 12.5
        elif uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI", "MA"]: frete = 22.9
        else: frete = 39.9
        if subtotal - desconto > 300 or tipo_cliente == "VIP": frete = 0

        total = subtotal - desconto + frete
        if pagamento == "PIX": total = total * 0.95
        elif pagamento == "BOLETO": total = total + 2.5
        elif pagamento == "CARTAO":
            if parcelas < 1 or parcelas > 12: return "ERRO: parcelas invalidas"
            if parcelas > 3: total = total * (1 + 0.0199 * parcelas)
        else: return "ERRO: forma de pagamento invalida"
        
        total = round(total * 100.0) / 100.0

        for item in self.itens:
            self.estoque[item[0]] = self.estoque[item[0]] - int(item[1])

        endereco = rua + ", " + numero + ", " + cidade + "/" + uf + ", CEP " + cep

        try:
            f = open("pedidos.csv", "a", encoding="utf-8")
            f.write(nome + ";" + email + ";" + tipo_cliente + ";" + pagamento + ";" + str(total) + ";" + endereco + "\n")
            f.close()
        except OSError as e:
            print("Falha ao salvar pedido: " + str(e))

        mensagem = "Ola " + nome + ", seu pedido foi confirmado. "
        if tipo_cliente == "VIP": mensagem += "Obrigado por ser VIP! Frete gratis garantido. "
        elif tipo_cliente == "FUNCIONARIO": mensagem += "Desconto de colaborador aplicado. "
        mensagem += "Total: R$ " + "%.2f" % total + ". Entrega em: " + endereco
        print("[EMAIL para " + email + "] " + mensagem)

        self.historico.append(nome + "|" + tipo_cliente + "|" + str(total))
        self.total_vendido += total
        self.itens.clear()
        return "OK: " + "%.2f" % total
