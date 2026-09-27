"""Janela principal do sistema (depois do login).

    ┌──────────────────────── barra de topo ────────────────────────┐
    │ marca · saudação · perfil                              [Sair] │
    ├──────────┬────────────────────────────────────────────────────┤
    │ sidebar  │ abas: [Registos] [Vendas]                          │
    │ (ações)  │ tabela + resumo                                    │
    └──────────┴────────────────────────────────────────────────────┘

Esta classe só trata da interface: as operações sobre dados estão em
ListaLigada / ListaVendas.

Para acrescentar uma operação:
  1. criar o método acao_... (diálogos com _nova_janela/_mostrar_janela);
  2. acrescentá-la à lista em _construir_sidebar;
  3. se for só do Dono: pô-la em OPERACOES_RESTRITAS_AO_DONO e chamar
     self._exige_dono() no início.
"""

import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from src.config import MOEDA, NOME_PADARIA, OPERACOES_RESTRITAS_AO_DONO, PERFIL_DONO
from src.estruturas import ListaLigada, ListaVendas
from src.interface.tema import centrar_janela, configurar_linhas_alternadas


class AplicacaoPadaria:

    # Atributos do produto, pela ordem em que aparecem na tabela, na janela
    # de produto e nas buscas. Têm de ter os mesmos nomes que em No.
    ATRIBUTOS = ["codigo", "nome", "categoria", "preco", "quantidade", "validade"]
    ATRIBUTOS_LABEL = {
        "codigo": "Código",
        "nome": "Nome",
        "categoria": "Categoria",
        "preco": "Preço",
        "quantidade": "Quantidade",
        "validade": "Validade",
    }
    # Dica mostrada ao lado do campo na janela de produto.
    ATRIBUTOS_DICA = {
        "preco": MOEDA,
        "validade": "dd/mm/aaaa",
    }

    LARGURA, ALTURA = 1150, 700
    LARGURA_MIN, ALTURA_MIN = 950, 600

    def __init__(self, root, perfil, ao_terminar_sessao):
        # Os dados vivem aqui e perdem-se ao sair. Para persistência, carregar
        # de um ficheiro em vez de _popular_exemplo.
        self.lista = ListaLigada()
        self.lista_vendas = ListaVendas()
        self.root = root
        self.perfil = perfil  # dict com "tipo" e "nome" do utilizador autenticado
        self.e_dono = perfil["tipo"] == PERFIL_DONO
        self.ao_terminar_sessao = ao_terminar_sessao

        self.root.title(f"{NOME_PADARIA} - Sistema de Gestão")
        self.root.resizable(True, True)
        self.root.minsize(self.LARGURA_MIN, self.ALTURA_MIN)
        centrar_janela(self.root, self.LARGURA, self.ALTURA)

        self._popular_exemplo()
        self._construir_layout()

    # ---------------- LAYOUT PRINCIPAL ----------------
    def _construir_layout(self):
        self._construir_barra_topo()  # primeiro, para ficar com o espaço do topo

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self._construir_sidebar()

        area = ttk.Frame(self.container, padding=(16, 14))
        area.pack(side="left", fill="both", expand=True)
        self._construir_abas(area)

    # ---------------- BARRA DE TOPO ----------------
    def _construir_barra_topo(self):
        topo = ttk.Frame(self.root, padding=(16, 10), style="Topo.TFrame")
        topo.pack(fill="x", side="top")

        ttk.Label(topo, text=f"🥖  {NOME_PADARIA}", style="TopoMarca.TLabel").pack(side="left")

        # side="right" enche da direita para o centro: o botão fica na ponta.
        ttk.Button(topo, text="Sair", style="Secundario.TButton",
                   command=self._terminar_sessao).pack(side="right")
        ttk.Label(topo, text=f"Perfil: {self.perfil['tipo']}",
                  style="TopoSuave.TLabel").pack(side="right", padx=(0, 16))
        ttk.Label(topo, text=self._saudacao(), style="Topo.TLabel").pack(side="right", padx=(0, 24))

    def _saudacao(self):
        hora = datetime.now().hour
        if hora < 12:
            inicio = "Bom dia"
        elif hora < 19:
            inicio = "Boa tarde"
        else:
            inicio = "Boa noite"
        return f"{inicio}, {self.perfil['nome']}! O forno já está quente 🔥"

    def _terminar_sessao(self):
        if messagebox.askyesno("Terminar sessão", "Deseja terminar a sessão actual?"):
            self.root.destroy()
            self.ao_terminar_sessao()

    # ---------------- SIDEBAR ----------------
    def _construir_sidebar(self):
        sidebar = ttk.Frame(self.container, width=230, style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)  # largura fixa

        titulo = ttk.Label(sidebar, text="Operações", style="Sidebar.TLabel")
        titulo.pack(pady=(18, 12), padx=16, anchor="w")

        # (identificador, método). O identificador é o texto do botão e é
        # comparado com OPERACOES_RESTRITAS_AO_DONO: mudar um obriga a mudar o outro.
        operacoes = [
            ("Buscar Produto", self.acao_buscar_produto),
            ("Registar Venda", self._registar_venda),
            ("Cadastrar", self.acao_cadastrar),
            ("Buscar (1 atributo)", self.acao_buscar_um_atributo),
            ("Buscar (2 atributos)", self.acao_buscar_dois_atributos),
            ("Alterar (por código)", self.acao_alterar),
            ("Eliminar por posição", self.acao_eliminar_posicao),
            ("Eliminar por código", self.acao_eliminar_codigo),
            ("Listar todos", self.acao_listar_todos),
            ("Listar por critério", self.acao_listar_criterio),
            ("Listar ordenado", self.acao_listar_ordenado),
        ]

        for identificador, comando in operacoes:
            restrita = identificador in OPERACOES_RESTRITAS_AO_DONO
            if restrita and not self.e_dono:
                continue  # operação nem sequer é apresentada a quem não é o Dono
            btn = ttk.Button(sidebar, text=identificador,
                             style="Sidebar.TButton", command=comando)
            btn.pack(fill="x", padx=8, pady=1)

    # ---------------- ABAS (REGISTOS / VENDAS) ----------------
    def _construir_abas(self, parent):
        self.abas = ttk.Notebook(parent)
        self.abas.pack(fill="both", expand=True)

        # --- Aba Registos: uma coluna por atributo ---
        self.tab_registos = ttk.Frame(self.abas)
        self.abas.add(self.tab_registos, text="🍞  Registos")

        colunas = self.ATRIBUTOS
        self.tabela_registos = ttk.Treeview(self.tab_registos, columns=colunas, show="headings")
        for atributo in colunas:
            self.tabela_registos.heading(atributo, text=self.ATRIBUTOS_LABEL[atributo])
            self.tabela_registos.column(atributo, width=120, anchor="center")
        configurar_linhas_alternadas(self.tabela_registos)
        self.tabela_registos.pack(fill="both", expand=True, side="left")

        scrollbar_r = ttk.Scrollbar(self.tab_registos, orient="vertical",
                                     command=self.tabela_registos.yview)
        self.tabela_registos.configure(yscrollcommand=scrollbar_r.set)
        scrollbar_r.pack(fill="y", side="right")

        # --- Aba Vendas ---
        self.tab_vendas = ttk.Frame(self.abas)
        self.abas.add(self.tab_vendas, text="🧾  Vendas")

        colunas_venda = ("data", "codigo", "nome", "quantidade", "preco_unit", "total")
        labels_venda = {
            "data": "Data",
            "codigo": "Código",
            "nome": "Produto",
            "quantidade": "Qtd Solicitada",
            "preco_unit": "Preço Unitário",
            "total": "Total",
        }

        # Resumo empacotado antes da tabela, para a tabela não o empurrar para fora.
        self.frame_resumo_vendas = ttk.Frame(self.tab_vendas, padding=(10, 8))
        self.frame_resumo_vendas.pack(fill="x", side="bottom")

        self.tabela_vendas = ttk.Treeview(self.tab_vendas, columns=colunas_venda, show="headings")
        for col in colunas_venda:
            self.tabela_vendas.heading(col, text=labels_venda[col])
            self.tabela_vendas.column(col, width=130, anchor="center")
        configurar_linhas_alternadas(self.tabela_vendas)
        self.tabela_vendas.pack(fill="both", expand=True, side="left")

        scrollbar_v = ttk.Scrollbar(self.tab_vendas, orient="vertical",
                                     command=self.tabela_vendas.yview)
        self.tabela_vendas.configure(yscrollcommand=scrollbar_v.set)
        scrollbar_v.pack(fill="y", side="right")

        self.label_total_qtd = ttk.Label(self.frame_resumo_vendas, text="Total Qtd: 0",
                                          style="Resumo.TLabel")
        self.label_total_qtd.pack(side="left", padx=(4, 24))

        self.label_total_vendas = ttk.Label(self.frame_resumo_vendas, text=f"Total Vendas: 0.00 {MOEDA}",
                                             style="Resumo.TLabel")
        self.label_total_vendas.pack(side="left")

        btn_registar = ttk.Button(self.frame_resumo_vendas, text="+ Registar Venda",
                                   command=self._registar_venda)
        btn_registar.pack(side="right")

        self._actualizar_tabela_registos()
        self._actualizar_tabela_vendas()

    # ---------------- DADOS DE EXEMPLO ----------------
    def _popular_exemplo(self):
        exemplos = [
            (1, "Pão de forma", "Pão", 80.0, 50, "15/09/2026"),
            (2, "Bolo de chocolate", "Bolo", 350.0, 10, "12/09/2026"),
            (3, "Pastel de nata", "Doce", 45.0, 30, "13/09/2026"),
            (4, "Pão careca", "Pão", 15.0, 100, "14/09/2026"),
        ]
        for e in exemplos:
            self.lista.cadastrar(*e)

        self.lista_vendas.registar_venda(1, "Pão de forma", 10, 80.0)
        self.lista_vendas.registar_venda(3, "Pastel de nata", 5, 45.0)
        self.lista_vendas.registar_venda(2, "Bolo de chocolate", 2, 350.0)

    # ---------------- ACTUALIZAR TABELAS ----------------
    # Apaga tudo e volta a inserir: simples, e rápido para centenas de linhas.

    def _actualizar_tabela_registos(self, produtos=None):
        """Sem argumento mostra todos os produtos; as buscas passam os resultados."""
        if produtos is None:
            produtos = self.lista.listar_todos()
        self.tabela_registos.delete(*self.tabela_registos.get_children())
        for i, p in enumerate(produtos):
            self.tabela_registos.insert(
                "", "end",
                values=[getattr(p, atributo) for atributo in self.ATRIBUTOS],
                tags=("par",) if i % 2 else (),
            )

    def _actualizar_tabela_vendas(self):
        vendas = self.lista_vendas.listar_todas()
        self.tabela_vendas.delete(*self.tabela_vendas.get_children())
        for i, v in enumerate(vendas):
            self.tabela_vendas.insert("", "end", values=(
                v.data, v.codigo_produto, v.nome_produto,
                v.quantidade, f"{v.preco_unitario:.2f}", f"{v.total:.2f}"
            ), tags=("par",) if i % 2 else ())
        self.label_total_qtd.config(text=f"Total Qtd: {self.lista_vendas.total_quantidade()}")
        self.label_total_vendas.config(text=f"Total Vendas: {self.lista_vendas.total_vendas():.2f} {MOEDA}")

    # ---------------- PERMISSÕES ----------------
    def _exige_dono(self):
        """Segunda linha de defesa (a sidebar já esconde os botões). Devolve
        True se a ação deve parar."""
        if not self.e_dono:
            messagebox.showwarning(
                "Acesso restrito",
                "Esta operação está reservada ao Dono da Padaria."
            )
            return True
        return False

    # ---------------- AÇÕES ----------------
    # As estruturas sinalizam erros com ValueError/IndexError, e as ações
    # apanham-nos e mostram-nos. Uma exceção não apanhada só aparece no
    # terminal, e o utilizador não vê nada.

    def acao_buscar_produto(self):
        janela, corpo = self._nova_janela("Buscar Produto")

        ttk.Label(corpo, text="Código do Produto:").grid(row=0, column=0, padx=(0, 10), pady=10)
        entrada_codigo = ttk.Entry(corpo, width=20)
        entrada_codigo.grid(row=0, column=1, pady=10)
        entrada_codigo.focus()

        def buscar():
            try:
                codigo = int(entrada_codigo.get().strip())
            except ValueError:
                messagebox.showwarning("Aviso", "Insira um código numérico válido.", parent=janela)
                return

            produto = self.lista.buscar_por_codigo(codigo)
            if produto is None:
                messagebox.showinfo("Resultado", f"Nenhum produto encontrado com código {codigo}.", parent=janela)
                return

            self._actualizar_tabela_registos([produto])
            self.abas.select(self.tab_registos)
            self.tabela_registos.selection_set(self.tabela_registos.get_children()[0])
            janela.destroy()

        entrada_codigo.bind("<Return>", lambda e: buscar())

        ttk.Button(corpo, text="Buscar", command=buscar).grid(row=1, column=0, columnspan=2, pady=(10, 0))
        self._mostrar_janela(janela)

    def acao_cadastrar(self):
        if self._exige_dono():
            return

        def gravar(dados, janela):
            try:
                codigo = int(dados["codigo"])
                preco = float(dados["preco"])
                quantidade = int(dados["quantidade"])
            except ValueError:
                messagebox.showerror("Erro", "Verifique os campos numéricos (código, preço, quantidade).",
                                     parent=janela)
                return False
            try:
                self.lista.cadastrar(codigo, dados["nome"], dados["categoria"],
                                     preco, quantidade, dados["validade"])
            except ValueError as e:  # ex.: código repetido
                messagebox.showerror("Erro", str(e), parent=janela)
                return False
            self._actualizar_tabela_registos()
            self.abas.select(self.tab_registos)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.", parent=janela)
            return True

        self._janela_produto("Cadastrar Produto", "Cadastrar", gravar)

    def acao_alterar(self):
        """Pede o código e abre a janela de produto já preenchida."""
        if self._exige_dono():
            return
        texto = self._pedir_valor_simples("Alterar Produto", "Código do produto:")
        if texto is None:
            return
        try:
            codigo = int(texto)
        except ValueError:
            messagebox.showwarning("Aviso", "Insira um código numérico válido.")
            return
        produto = self.lista.buscar_por_codigo(codigo)
        if produto is None:
            messagebox.showerror("Erro", f"Produto com código {codigo} não encontrado.")
            return

        def gravar(dados, janela):
            try:
                # Campos numéricos vazios passam como None e são ignorados.
                novos_dados = {
                    "nome": dados["nome"],
                    "categoria": dados["categoria"],
                    "preco": float(dados["preco"]) if dados["preco"] else None,
                    "quantidade": int(dados["quantidade"]) if dados["quantidade"] else None,
                    "validade": dados["validade"],
                }
            except ValueError:
                messagebox.showerror("Erro", "Preço e quantidade têm de ser numéricos.", parent=janela)
                return False
            self.lista.alterar_por_codigo(codigo, novos_dados)
            self._actualizar_tabela_registos()
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso.", parent=janela)
            return True

        self._janela_produto(f"Alterar Produto {codigo}", "Guardar alterações", gravar, produto)

    def acao_buscar_um_atributo(self):
        atributo, valor = self._pedir_atributo_valor("Buscar por 1 atributo")
        if atributo is None:
            return
        resultados = self.lista.buscar_por_um_atributo(atributo, valor)
        self._actualizar_tabela_registos(resultados)
        self.abas.select(self.tab_registos)
        if not resultados:
            messagebox.showinfo("Busca", "Nenhum produto encontrado.")

    def acao_buscar_dois_atributos(self):
        janela, corpo = self._nova_janela("Buscar por 2 atributos")

        ttk.Label(corpo, text="Atributo 1:").grid(row=0, column=0, padx=5, pady=6, sticky="e")
        combo1 = self._combo_atributos(corpo)
        combo1.grid(row=0, column=1, padx=5, pady=6)
        entrada1 = ttk.Entry(corpo)
        entrada1.grid(row=0, column=2, padx=5, pady=6)

        ttk.Label(corpo, text="Atributo 2:").grid(row=1, column=0, padx=5, pady=6, sticky="e")
        combo2 = self._combo_atributos(corpo)
        combo2.grid(row=1, column=1, padx=5, pady=6)
        entrada2 = ttk.Entry(corpo)
        entrada2.grid(row=1, column=2, padx=5, pady=6)

        def confirmar():
            atributo1 = self._atributo_escolhido(combo1)
            atributo2 = self._atributo_escolhido(combo2)
            if atributo1 is None or atributo2 is None:
                messagebox.showwarning("Aviso", "Escolha os dois atributos.", parent=janela)
                return
            resultados = self.lista.buscar_por_dois_atributos(
                atributo1, entrada1.get(), atributo2, entrada2.get()
            )
            self._actualizar_tabela_registos(resultados)
            self.abas.select(self.tab_registos)
            janela.destroy()
            if not resultados:
                messagebox.showinfo("Busca", "Nenhum produto encontrado.")

        ttk.Button(corpo, text="Buscar", command=confirmar).grid(row=2, column=0, columnspan=3, pady=(12, 0))
        self._mostrar_janela(janela)

    def acao_eliminar_posicao(self):
        if self._exige_dono():
            return
        posicao = self._pedir_valor_simples("Eliminar por posição", "Posição (1 = primeiro):")
        if posicao is None:
            return
        try:
            removido = self.lista.eliminar_por_posicao(int(posicao))
            self._actualizar_tabela_registos()
            messagebox.showinfo("Sucesso", f"Produto '{removido.nome}' eliminado.")
        except (ValueError, IndexError) as e:
            messagebox.showerror("Erro", str(e))

    def acao_eliminar_codigo(self):
        if self._exige_dono():
            return
        codigo = self._pedir_valor_simples("Eliminar por código", "Código:")
        if codigo is None:
            return
        try:
            removido = self.lista.eliminar_por_codigo(int(codigo))
            self._actualizar_tabela_registos()
            messagebox.showinfo("Sucesso", f"Produto '{removido.nome}' eliminado.")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def acao_listar_todos(self):
        self._actualizar_tabela_registos()
        self.abas.select(self.tab_registos)

    def acao_listar_criterio(self):
        atributo, valor = self._pedir_atributo_valor("Listar por critério")
        if atributo is None:
            return
        resultados = self.lista.listar_por_criterio(atributo, valor)
        self._actualizar_tabela_registos(resultados)
        self.abas.select(self.tab_registos)

    def acao_listar_ordenado(self):
        janela, corpo = self._nova_janela("Listar ordenado")

        ttk.Label(corpo, text="Ordenar por:").grid(row=0, column=0, padx=5, pady=6)
        combo = self._combo_atributos(corpo)
        combo.grid(row=0, column=1, padx=5, pady=6)

        decrescente_var = tk.BooleanVar()
        ttk.Checkbutton(corpo, text="Ordem decrescente", variable=decrescente_var).grid(
            row=1, column=0, columnspan=2, pady=6
        )

        def confirmar():
            atributo = self._atributo_escolhido(combo)
            if atributo is None:
                messagebox.showwarning("Aviso", "Escolha o atributo para ordenar.", parent=janela)
                return
            resultados = self.lista.listar_ordenado(atributo, decrescente_var.get())
            self._actualizar_tabela_registos(resultados)
            self.abas.select(self.tab_registos)
            janela.destroy()

        ttk.Button(corpo, text="Ordenar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=(12, 0))
        self._mostrar_janela(janela)

    # ---------------- REGISTAR VENDA ----------------
    def _registar_venda(self):
        """As regras da venda (quantidade > 0, produto existe, stock chega) estão aqui."""
        janela, corpo = self._nova_janela("Registar Venda")

        ttk.Label(corpo, text="Código do Produto:").grid(row=0, column=0, padx=(0, 10), pady=8, sticky="e")
        entrada_codigo = ttk.Entry(corpo, width=25)
        entrada_codigo.grid(row=0, column=1, pady=8)
        entrada_codigo.focus()

        ttk.Label(corpo, text="Quantidade:").grid(row=1, column=0, padx=(0, 10), pady=8, sticky="e")
        entrada_qtd = ttk.Entry(corpo, width=25)
        entrada_qtd.grid(row=1, column=1, pady=8)

        def confirmar():
            try:
                codigo = int(entrada_codigo.get().strip())
                qtd = int(entrada_qtd.get().strip())
                if qtd <= 0:
                    raise ValueError("Quantidade deve ser maior que 0.")
            except ValueError:
                messagebox.showwarning("Aviso", "Código e quantidade devem ser numéricos positivos.", parent=janela)
                return

            produto = self.lista.buscar_por_codigo(codigo)
            if produto is None:
                messagebox.showerror("Erro", f"Produto com código {codigo} não encontrado.", parent=janela)
                return

            if qtd > produto.quantidade:
                messagebox.showwarning("Aviso",
                    f"Estoque insuficiente. Disponível: {produto.quantidade}", parent=janela)
                return

            # Só desconta o stock depois de todas as validações passarem.
            produto.quantidade -= qtd
            self.lista_vendas.registar_venda(codigo, produto.nome, qtd, produto.preco)
            self._actualizar_tabela_registos()
            self._actualizar_tabela_vendas()
            self.abas.select(self.tab_vendas)
            messagebox.showinfo("Sucesso",
                f"Venda registada: {qtd}x {produto.nome} = {qtd * produto.preco:.2f} {MOEDA}", parent=janela)
            janela.destroy()

        entrada_codigo.bind("<Return>", lambda e: entrada_qtd.focus())
        entrada_qtd.bind("<Return>", lambda e: confirmar())

        ttk.Button(corpo, text="Registar Venda", command=confirmar).grid(
            row=2, column=0, columnspan=2, pady=(14, 0))
        self._mostrar_janela(janela)

    # ---------------- JANELAS AUXILIARES ----------------
    # Todos os diálogos: _nova_janela -> widgets em `corpo` -> _mostrar_janela.

    def _nova_janela(self, titulo):
        """Devolve (janela, corpo). Os widgets vão para `corpo`, que já tem margens."""
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.resizable(False, False)
        janela.transient(self.root)  # fica sempre por cima da janela principal
        corpo = ttk.Frame(janela, padding=24)
        corpo.pack(fill="both", expand=True)
        return janela, corpo

    def _mostrar_janela(self, janela):
        """Centra e torna modal. Chamar depois de criar os widgets."""
        centrar_janela(janela)
        janela.grab_set()

    def _janela_produto(self, titulo, texto_botao, ao_confirmar, produto=None):
        """Janela com um campo por atributo, usada por Cadastrar e Alterar.

        Com `produto`, os campos vêm preenchidos e o código fica bloqueado.
        ao_confirmar(dados, janela) recebe {atributo: texto} e devolve True
        para fechar a janela, ou False para a manter aberta (ex.: erro).
        """
        janela, corpo = self._nova_janela(titulo)
        ttk.Label(corpo, text=titulo, style="Seccao.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

        entradas = {}
        for linha, atributo in enumerate(self.ATRIBUTOS, start=1):
            ttk.Label(corpo, text=self.ATRIBUTOS_LABEL[atributo] + ":").grid(
                row=linha, column=0, sticky="e", padx=(0, 10), pady=5)
            entrada = ttk.Entry(corpo, width=28)
            entrada.grid(row=linha, column=1, pady=5)
            if produto is not None:
                entrada.insert(0, str(getattr(produto, atributo)))
            dica = self.ATRIBUTOS_DICA.get(atributo)
            if dica:
                ttk.Label(corpo, text=dica, style="Suave.TLabel").grid(
                    row=linha, column=2, sticky="w", padx=(8, 0))
            entradas[atributo] = entrada

        if produto is not None:
            entradas["codigo"].state(["disabled"])  # o código identifica o produto
            entradas["nome"].focus()
        else:
            entradas["codigo"].focus()

        def confirmar():
            dados = {a: e.get().strip() for a, e in entradas.items()}
            if ao_confirmar(dados, janela):
                janela.destroy()

        janela.bind("<Return>", lambda e: confirmar())
        ttk.Button(corpo, text=texto_botao, command=confirmar).grid(
            row=len(self.ATRIBUTOS) + 1, column=0, columnspan=3, sticky="ew", pady=(18, 0))
        self._mostrar_janela(janela)

    def _combo_atributos(self, parent):
        """Combobox com nomes amigáveis ("Preço"); ler com _atributo_escolhido."""
        return ttk.Combobox(parent, state="readonly",
                            values=[self.ATRIBUTOS_LABEL[a] for a in self.ATRIBUTOS])

    def _atributo_escolhido(self, combo):
        """Nome interno do atributo escolhido ("preco"), ou None."""
        indice = combo.current()  # -1 sem seleção
        return self.ATRIBUTOS[indice] if indice >= 0 else None

    def _pedir_atributo_valor(self, titulo):
        """Bloqueia até a janela fechar. Devolve (atributo, valor), ou
        (None, None) se o utilizador fechar sem confirmar."""
        janela, corpo = self._nova_janela(titulo)
        resultado = {"atributo": None, "valor": None}  # dict: confirmar() pode alterá-lo

        ttk.Label(corpo, text="Atributo:").grid(row=0, column=0, padx=5, pady=6, sticky="e")
        combo = self._combo_atributos(corpo)
        combo.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(corpo, text="Valor:").grid(row=1, column=0, padx=5, pady=6, sticky="e")
        entrada = ttk.Entry(corpo)
        entrada.grid(row=1, column=1, padx=5, pady=6)

        def confirmar():
            atributo = self._atributo_escolhido(combo)
            if atributo is None:
                messagebox.showwarning("Aviso", "Escolha um atributo.", parent=janela)
                return
            resultado["atributo"] = atributo
            resultado["valor"] = entrada.get()
            janela.destroy()

        entrada.bind("<Return>", lambda e: confirmar())
        ttk.Button(corpo, text="Confirmar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=(12, 0))
        self._mostrar_janela(janela)
        self.root.wait_window(janela)

        return resultado["atributo"], resultado["valor"]

    def _pedir_valor_simples(self, titulo, label_texto):
        """Como _pedir_atributo_valor, só com um campo. Devolve o texto ou None."""
        janela, corpo = self._nova_janela(titulo)
        resultado = {"valor": None}

        ttk.Label(corpo, text=label_texto).grid(row=0, column=0, padx=5, pady=6)
        entrada = ttk.Entry(corpo)
        entrada.grid(row=0, column=1, padx=5, pady=6)
        entrada.focus()

        def confirmar():
            resultado["valor"] = entrada.get()
            janela.destroy()

        entrada.bind("<Return>", lambda e: confirmar())
        ttk.Button(corpo, text="Confirmar", command=confirmar).grid(row=1, column=0, columnspan=2, pady=(12, 0))
        self._mostrar_janela(janela)
        self.root.wait_window(janela)

        return resultado["valor"]
