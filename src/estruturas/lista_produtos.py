"""Lista duplamente ligada que guarda os produtos da padaria.

Invariantes (qualquer método que mexa em ligações tem de as manter):
  - lista vazia <=> primeiro is None <=> ultimo is None <=> tamanho == 0
  - primeiro.anterior is None e ultimo.proximo is None
  - n.proximo.anterior is n, para todo o nó n com próximo

Para escalar: um dicionário {codigo: No} ao lado da lista tornaria as
buscas por código O(1) em vez de O(n).
"""


class No:
    """Um produto + ligações ao nó anterior e ao próximo.

    Para acrescentar um atributo: pô-lo aqui e em ListaLigada.cadastrar, e
    depois em AplicacaoPadaria.ATRIBUTOS / ATRIBUTOS_LABEL.
    """

    def __init__(self, codigo, nome, categoria, preco, quantidade, validade):
        self.codigo = codigo            # int, único na lista
        self.nome = nome
        self.categoria = categoria
        self.preco = preco              # float
        self.quantidade = quantidade    # int, stock disponível
        self.validade = validade        # str "dd/mm/aaaa"
        self.anterior = None
        self.proximo = None


class ListaLigada:
    """Lista duplamente ligada que armazena os produtos da padaria."""

    def __init__(self):
        self.primeiro = None
        self.ultimo = None     # permite inserir no fim em O(1)
        self.tamanho = 0

    # ---------------- CADASTRO ----------------
    def cadastrar(self, codigo, nome, categoria, preco, quantidade, validade):
        """Insere no fim. O código tem de ser único (é a chave de tudo o resto)."""
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Já existe um produto com o código {codigo}.")

        novo_no = No(codigo, nome, categoria, preco, quantidade, validade)
        if self.primeiro is None:
            self.primeiro = novo_no
            self.ultimo = novo_no
        else:
            novo_no.anterior = self.ultimo
            self.ultimo.proximo = novo_no
            self.ultimo = novo_no
        self.tamanho += 1

    # ---------------- BUSCA ----------------
    def buscar_por_codigo(self, codigo):
        actual = self.primeiro
        while actual is not None:
            if actual.codigo == codigo:
                return actual
            actual = actual.proximo
        return None

    def buscar_por_um_atributo(self, atributo, valor):
        """`atributo` é o nome do campo (ex.: "categoria"), lido com getattr.
        Compara como texto, sem distinguir maiúsculas. Por isso o preço 15
        só é encontrado escrevendo "15.0"."""
        resultados = []
        actual = self.primeiro
        valor = str(valor).strip().lower()
        while actual is not None:
            valor_atributo = str(getattr(actual, atributo)).strip().lower()
            if valor_atributo == valor:
                resultados.append(actual)
            actual = actual.proximo
        return resultados

    def buscar_por_dois_atributos(self, atributo1, valor1, atributo2, valor2):
        """As duas condições têm de se verificar (E lógico)."""
        resultados = []
        actual = self.primeiro
        valor1 = str(valor1).strip().lower()
        valor2 = str(valor2).strip().lower()
        while actual is not None:
            v1 = str(getattr(actual, atributo1)).strip().lower()
            v2 = str(getattr(actual, atributo2)).strip().lower()
            if v1 == valor1 and v2 == valor2:
                resultados.append(actual)
            actual = actual.proximo
        return resultados

    # ---------------- ALTERAÇÃO ----------------
    def alterar_por_codigo(self, codigo, novos_dados: dict):
        """Valores None ou "" são ignorados (o campo mantém o valor atual)."""
        no = self.buscar_por_codigo(codigo)
        if no is None:
            raise ValueError(f"Produto com código {codigo} não encontrado.")
        for chave, valor in novos_dados.items():
            if valor not in (None, ""):
                setattr(no, chave, valor)
        return no

    # ---------------- ELIMINAÇÃO ----------------
    def _desligar(self, no):
        """Retira o nó da lista, religando o anterior e o próximo entre si.
        Único sítio que remove nós: novas formas de eliminar devem usá-lo."""
        if no.anterior is None:
            self.primeiro = no.proximo
        else:
            no.anterior.proximo = no.proximo

        if no.proximo is None:
            self.ultimo = no.anterior
        else:
            no.proximo.anterior = no.anterior

        no.anterior = None
        no.proximo = None
        self.tamanho -= 1
        return no

    def eliminar_por_posicao(self, posicao):
        """Posição começa em 1."""
        if posicao < 1 or posicao > self.tamanho:
            raise IndexError("Posição inválida.")

        # Percorre a partir da extremidade mais próxima da posição pedida
        if posicao <= self.tamanho // 2:
            actual = self.primeiro
            for _ in range(posicao - 1):
                actual = actual.proximo
        else:
            actual = self.ultimo
            for _ in range(self.tamanho - posicao):
                actual = actual.anterior
        return self._desligar(actual)

    def eliminar_por_codigo(self, codigo):
        if self.primeiro is None:
            raise ValueError("A lista está vazia.")

        no = self.buscar_por_codigo(codigo)
        if no is None:
            raise ValueError(f"Produto com código {codigo} não encontrado.")
        return self._desligar(no)

    # ---------------- IMPRESSÃO ----------------
    # Devolvem os próprios nós (não cópias): quem os usa não deve mexer em
    # anterior/proximo.

    def listar_todos(self):
        produtos = []
        actual = self.primeiro
        while actual is not None:
            produtos.append(actual)
            actual = actual.proximo
        return produtos

    def listar_por_criterio(self, atributo, valor):
        return self.buscar_por_um_atributo(atributo, valor)

    def listar_ordenado(self, atributo, decrescente=False):
        """Bubble sort sobre uma cópia, e a lista ligada não muda.

        Limite: `validade` é texto, por isso "01/12/2026" fica antes de
        "15/09/2026". Para ordenar datas bem, guardar como datetime.date.
        """
        produtos = self.listar_todos()
        n = len(produtos)
        for i in range(n):
            for j in range(0, n - i - 1):
                v1 = getattr(produtos[j], atributo)
                v2 = getattr(produtos[j + 1], atributo)
                if (v1 > v2 and not decrescente) or (v1 < v2 and decrescente):
                    produtos[j], produtos[j + 1] = produtos[j + 1], produtos[j]
        return produtos
