"""Lista duplamente ligada que guarda os produtos da padaria."""


class No:
    """Nó da lista duplamente ligada. Cada nó guarda um produto e as referências
    ao nó anterior e ao próximo nó."""

    def __init__(self, codigo, nome, categoria, preco, quantidade, validade):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        self.validade = validade
        self.anterior = None
        self.proximo = None


class ListaLigada:
    """Lista duplamente ligada que armazena os produtos da padaria."""

    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    # ---------------- CADASTRO ----------------
    def cadastrar(self, codigo, nome, categoria, preco, quantidade, validade):
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Já existe um produto com o código {codigo}.")

        novo_no = No(codigo, nome, categoria, preco, quantidade, validade)
        if self.cabeca is None:
            self.cabeca = novo_no
            self.cauda = novo_no
        else:
            novo_no.anterior = self.cauda
            self.cauda.proximo = novo_no
            self.cauda = novo_no
        self.tamanho += 1

    # ---------------- BUSCA ----------------
    def buscar_por_codigo(self, codigo):
        atual = self.cabeca
        while atual is not None:
            if atual.codigo == codigo:
                return atual
            atual = atual.proximo
        return None

    def buscar_por_um_atributo(self, atributo, valor):
        resultados = []
        atual = self.cabeca
        valor = str(valor).strip().lower()
        while atual is not None:
            valor_atributo = str(getattr(atual, atributo)).strip().lower()
            if valor_atributo == valor:
                resultados.append(atual)
            atual = atual.proximo
        return resultados

    def buscar_por_dois_atributos(self, atributo1, valor1, atributo2, valor2):
        resultados = []
        atual = self.cabeca
        valor1 = str(valor1).strip().lower()
        valor2 = str(valor2).strip().lower()
        while atual is not None:
            v1 = str(getattr(atual, atributo1)).strip().lower()
            v2 = str(getattr(atual, atributo2)).strip().lower()
            if v1 == valor1 and v2 == valor2:
                resultados.append(atual)
            atual = atual.proximo
        return resultados

    # ---------------- ALTERAÇÃO ----------------
    def alterar_por_codigo(self, codigo, novos_dados: dict):
        no = self.buscar_por_codigo(codigo)
        if no is None:
            raise ValueError(f"Produto com código {codigo} não encontrado.")
        for chave, valor in novos_dados.items():
            if valor not in (None, ""):
                setattr(no, chave, valor)
        return no

    # ---------------- ELIMINAÇÃO ----------------
    def _desligar(self, no):
        """Retira o nó da lista, religando o anterior e o próximo entre si."""
        if no.anterior is None:
            self.cabeca = no.proximo
        else:
            no.anterior.proximo = no.proximo

        if no.proximo is None:
            self.cauda = no.anterior
        else:
            no.proximo.anterior = no.anterior

        no.anterior = None
        no.proximo = None
        self.tamanho -= 1
        return no

    def eliminar_por_posicao(self, posicao):
        if posicao < 1 or posicao > self.tamanho:
            raise IndexError("Posição inválida.")

        # Percorre a partir da extremidade mais próxima da posição pedida
        if posicao <= self.tamanho // 2:
            atual = self.cabeca
            for _ in range(posicao - 1):
                atual = atual.proximo
        else:
            atual = self.cauda
            for _ in range(self.tamanho - posicao):
                atual = atual.anterior
        return self._desligar(atual)

    def eliminar_por_codigo(self, codigo):
        if self.cabeca is None:
            raise ValueError("A lista está vazia.")

        no = self.buscar_por_codigo(codigo)
        if no is None:
            raise ValueError(f"Produto com código {codigo} não encontrado.")
        return self._desligar(no)

    # ---------------- IMPRESSÃO ----------------
    def listar_todos(self):
        produtos = []
        atual = self.cabeca
        while atual is not None:
            produtos.append(atual)
            atual = atual.proximo
        return produtos

    def listar_por_criterio(self, atributo, valor):
        return self.buscar_por_um_atributo(atributo, valor)

    def listar_ordenado(self, atributo, decrescente=False):
        produtos = self.listar_todos()
        n = len(produtos)
        for i in range(n):
            for j in range(0, n - i - 1):
                v1 = getattr(produtos[j], atributo)
                v2 = getattr(produtos[j + 1], atributo)
                if (v1 > v2 and not decrescente) or (v1 < v2 and decrescente):
                    produtos[j], produtos[j + 1] = produtos[j + 1], produtos[j]
        return produtos
