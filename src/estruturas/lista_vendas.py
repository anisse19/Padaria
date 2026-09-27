"""Lista ligada que guarda as vendas realizadas."""

from datetime import datetime


class NoVenda:
    """Nó da lista ligada de vendas."""

    def __init__(self, codigo_produto, nome_produto, quantidade, preco_unitario):
        self.codigo_produto = codigo_produto
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = quantidade * preco_unitario
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.proximo = None


class ListaVendas:
    """Lista ligada que armazena as vendas realizadas."""

    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def registar_venda(self, codigo_produto, nome_produto, quantidade, preco_unitario):
        novo_no = NoVenda(codigo_produto, nome_produto, quantidade, preco_unitario)
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self.tamanho += 1
        return novo_no

    def listar_todas(self):
        vendas = []
        atual = self.cabeca
        while atual is not None:
            vendas.append(atual)
            atual = atual.proximo
        return vendas

    def total_vendas(self):
        total = 0
        atual = self.cabeca
        while atual is not None:
            total += atual.total
            atual = atual.proximo
        return total

    def total_quantidade(self):
        total = 0
        atual = self.cabeca
        while atual is not None:
            total += atual.quantidade
            atual = atual.proximo
        return total
