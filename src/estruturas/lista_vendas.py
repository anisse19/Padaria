"""Lista duplamente ligada que guarda as vendas realizadas.

Só se acrescenta: as vendas não se alteram nem se apagam (histórico de caixa).
Se aparecer uma terceira lista, vale a pena extrair uma classe base comum
com ListaLigada, porque a inserção e o percurso são iguais.
"""

from datetime import datetime


class NoVenda:
    """Guarda uma cópia do nome e do preço no momento da venda, para o
    histórico não mudar se o produto for alterado ou eliminado depois."""

    def __init__(self, codigo_produto, nome_produto, quantidade, preco_unitario):
        self.codigo_produto = codigo_produto
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = quantidade * preco_unitario
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.anterior = None
        self.proximo = None


class ListaVendas:
    """Lista duplamente ligada que armazena as vendas realizadas."""

    def __init__(self):
        self.primeiro = None
        self.ultimo = None
        self.tamanho = 0

    def registar_venda(self, codigo_produto, nome_produto, quantidade, preco_unitario):
        """Não valida stock: essa regra está em AplicacaoPadaria._registar_venda."""
        novo_no = NoVenda(codigo_produto, nome_produto, quantidade, preco_unitario)
        if self.primeiro is None:
            self.primeiro = novo_no
            self.ultimo = novo_no
        else:
            novo_no.anterior = self.ultimo
            self.ultimo.proximo = novo_no
            self.ultimo = novo_no
        self.tamanho += 1
        return novo_no

    def listar_todas(self):
        vendas = []
        actual = self.primeiro
        while actual is not None:
            vendas.append(actual)
            actual = actual.proximo
        return vendas

    def total_vendas(self):
        total = 0
        actual = self.primeiro
        while actual is not None:
            total += actual.total
            actual = actual.proximo
        return total

    def total_quantidade(self):
        total = 0
        actual = self.primeiro
        while actual is not None:
            total += actual.quantidade
            actual = actual.proximo
        return total
