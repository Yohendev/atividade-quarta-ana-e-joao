from typing import Optional, List, Dict

class ItemPedido:
    def __init__(self, produto: str, quantidade: int, preco: float):
        self.produto = produto
        self.quantidade = int(quantidade)
        self.preco = float(preco)
    def calcular_subtotal(self) -> float:
        return self.quantidade * self.preco

class Cliente:
    def __init__(self, nome: str, email: str, tipo: str):
        self.nome = nome; self.email = email; self.tipo = tipo
    def is_valido(self) -> Optional[str]:
        if not self.nome or not self.nome.strip(): return "ERRO: cliente sem nome"
        if not self.email or "@" not in self.email or "." not in self.email: return "ERRO: email invalido"
        if self.tipo not in ["COMUM", "VIP", "FUNCIONARIO"]: return "ERRO: tipo de cliente desconhecido"
        return None

class Endereco:
    def __init__(self, rua: str, numero: str, cidade: str, uf: str, cep: str):
        self.rua = rua; self.numero = numero; self.cidade = cidade; self.uf = uf; self.cep = cep
    def is_valido(self) -> Optional[str]:
        if not self.cep or len(self.cep.replace("-", "")) != 8: return "ERRO: cep invalido"
        return None
    def formatar(self) -> str:
        return f"{self.rua}, {self.numero}, {self.cidade}/{self.uf}, CEP {self.cep}"

class CalculadoraPreco:
    @staticmethod
    def calcular_desconto(tipo_cliente: str, subtotal: float) -> float:
        if tipo_cliente == "COMUM" and subtotal > 500: return subtotal * 0.05
        if tipo_cliente == "VIP": return subtotal * 0.15 if subtotal > 500 else subtotal * 0.10
        if tipo_cliente == "FUNCIONARIO": return subtotal * 0.20
        return 0.0

    @staticmethod
    def calcular_frete(uf: str, total_com_desconto: float, tipo_cliente: str) -> float:
        if total_com_desconto > 300 or tipo_cliente == "VIP": return 0.0
        if uf == "PE": return 12.5
        if uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI", "MA"]: return 22.9
        return 39.9

    @staticmethod
    def aplicar_taxas_pagamento(total: float, pagamento: str, parcelas: int) -> float:
        if pagamento == "PIX": return total * 0.95
        if pagamento == "BOLETO": return total + 2.5
        if pagamento == "CARTAO":
            if parcelas < 1 or parcelas > 12: raise ValueError("ERRO: parcelas invalidas")
            if parcelas > 3: return total * (1 + 0.0199 * parcelas)
        elif pagamento not in ["PIX", "BOLETO", "CARTAO"]: raise ValueError("ERRO: forma de pagamento invalida")
        return total

class RepositorioPedidosCSV:
    @staticmethod
    def salvar(linha: str):
        try:
            with open("pedidos.csv", "a", encoding="utf-8") as f: f.write(linha + "\n")
        except OSError as e: print("Falha ao salvar pedido: " + str(e))

class ServicoNotificacao:
    @staticmethod
    def confirmar_pedido(cliente: Cliente, total: float, endereco: str):
        mensagem = f"Ola {cliente.nome}, seu pedido foi confirmado. "
        if cliente.tipo == "VIP": mensagem += "Obrigado por ser VIP! Frete gratis garantido. "
        elif cliente.tipo == "FUNCIONARIO": mensagem += "Desconto de colaborador aplicado. "
        mensagem += f"Total: R$ {total:.2f}. Entrega em: {endereco}"
        print(f"[EMAIL para {cliente.email}] {mensagem}")

class GerenciadorPedidos:
    def __init__(self):
        self.itens: List[ItemPedido] = []
        self.estoque: Dict[str, int] = {"CANETA": 100, "CADERNO": 50, "MOCHILA": 10, "CALCULADORA": 5}
        self.historico: List[str] = []
        self.total_vendido: float = 0

    def adicionar_item(self, produto: str, qtd: int, preco: float):
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
