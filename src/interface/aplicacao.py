"""Janela principal do sistema (depois do login)."""

import tkinter as tk
from tkinter import ttk, messagebox

from src.config import OPERACOES_RESTRITAS_AO_DONO
from src.estruturas import ListaLigada, ListaVendas


class AplicacaoPadaria:

    ATRIBUTOS = ["codigo", "nome", "categoria", "preco", "quantidade", "validade"]
    ATRIBUTOS_LABEL = {
        "codigo": "Código",
        "nome": "Nome",
        "categoria": "Categoria",
        "preco": "Preço",
        "quantidade": "Quantidade",
        "validade": "Validade",
    }

    def __init__(self, root, perfil, ao_terminar_sessao):
        self.lista = ListaLigada()
        self.lista_vendas = ListaVendas()
        self.root = root
        self.perfil = perfil  # dict com "tipo" e "nome" do utilizador autenticado
        self.e_dono = perfil["tipo"] == "Dono da Padaria"
        self.ao_terminar_sessao = ao_terminar_sessao  # volta à tela inicial

        self.root.title("Sistema de Gestão de Padaria")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        self._popular_exemplo()
        self._construir_layout()

    # ---------------- LAYOUT PRINCIPAL ----------------
    def _construir_layout(self):
        self._construir_barra_topo()

        # Container principal: sidebar à esquerda, conteúdo à direita
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self._construir_sidebar()
        self._construir_area_conteudo()

    # ---------------- BARRA DE TOPO (UTILIZADOR / SAIR) ----------------
    def _construir_barra_topo(self):
        topo = ttk.Frame(self.root, padding=(10, 6))
        topo.pack(fill="x", side="top")

        texto = f"Sessão: {self.perfil['nome']}  ·  Perfil: {self.perfil['tipo']}"
        ttk.Label(topo, text=texto, font=("Segoe UI", 9, "bold")).pack(side="left")

        ttk.Button(topo, text="Sair", command=self._terminar_sessao).pack(side="right")

    def _terminar_sessao(self):
        if messagebox.askyesno("Terminar sessão", "Deseja terminar a sessão actual?"):
            self.root.destroy()
            self.ao_terminar_sessao()

    # ---------------- SIDEBAR (BARRA LATERAL) ----------------
    def _construir_sidebar(self):
        sidebar = ttk.Frame(self.container, width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 2))
        sidebar.pack_propagate(False)

        titulo = ttk.Label(sidebar, text="Operações", font=("Segoe UI", 12, "bold"))
        titulo.pack(pady=(10, 15), padx=10)

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

        for texto, comando in operacoes:
            restrita = texto in OPERACOES_RESTRITAS_AO_DONO
            if restrita and not self.e_dono:
                continue  # operação nem sequer é apresentada a quem não é o Dono
            btn = ttk.Button(sidebar, text=texto, command=comando)
            btn.pack(fill="x", padx=8, pady=3)

    # ---------------- ÁREA DE CONTEÚDO ----------------
    def _construir_area_conteudo(self):
        area = ttk.Frame(self.container)
        area.pack(side="left", fill="both", expand=True)

        # Formulário de dados do produto (topo)
        self._construir_formulario(area)

        # Abas inferiores (Registos / Vendas)
        self._construir_abas(area)

    # ---------------- FORMULÁRIO DE ENTRADA ----------------
    def _construir_formulario(self, parent):
        frame = ttk.LabelFrame(parent, text="Dados do Produto")
        frame.pack(fill="x", padx=10, pady=(10, 5))

        self.entradas = {}
        for i, atributo in enumerate(self.ATRIBUTOS):
            label = ttk.Label(frame, text=self.ATRIBUTOS_LABEL[atributo] + ":")
            label.grid(row=i // 3, column=(i % 3) * 2, sticky="e", padx=5, pady=5)
            entrada = ttk.Entry(frame, width=20)
            entrada.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=5)
            self.entradas[atributo] = entrada

    # ---------------- ABAS INFERIORES (REGISTOS / VENDAS) ----------------
    def _construir_abas(self, parent):
        self.abas = ttk.Notebook(parent)
        self.abas.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # --- Aba Registos ---
        self.tab_registos = ttk.Frame(self.abas)
        self.abas.add(self.tab_registos, text="  Registos  ")

        colunas = self.ATRIBUTOS
        self.tabela_registos = ttk.Treeview(self.tab_registos, columns=colunas, show="headings")
        for atributo in colunas:
            self.tabela_registos.heading(atributo, text=self.ATRIBUTOS_LABEL[atributo])
            self.tabela_registos.column(atributo, width=120, anchor="center")
        self.tabela_registos.pack(fill="both", expand=True, side="left")

        scrollbar_r = ttk.Scrollbar(self.tab_registos, orient="vertical",
                                     command=self.tabela_registos.yview)
        self.tabela_registos.configure(yscrollcommand=scrollbar_r.set)
        scrollbar_r.pack(fill="y", side="right")

        # --- Aba Vendas ---
        self.tab_vendas = ttk.Frame(self.abas)
        self.abas.add(self.tab_vendas, text="  Vendas  ")

        colunas_venda = ("data", "codigo", "nome", "quantidade", "preco_unit", "total")
        labels_venda = {
            "data": "Data",
            "codigo": "Código",
            "nome": "Produto",
            "quantidade": "Qtd Solicitada",
            "preco_unit": "Preço Unitário",
            "total": "Total",
        }

        self.tabela_vendas = ttk.Treeview(self.tab_vendas, columns=colunas_venda, show="headings")
        for col in colunas_venda:
            self.tabela_vendas.heading(col, text=labels_venda[col])
            self.tabela_vendas.column(col, width=130, anchor="center")
        self.tabela_vendas.pack(fill="both", expand=True, side="left")

        scrollbar_v = ttk.Scrollbar(self.tab_vendas, orient="vertical",
                                     command=self.tabela_vendas.yview)
        self.tabela_vendas.configure(yscrollcommand=scrollbar_v.set)
        scrollbar_v.pack(fill="y", side="right")

        # Frame de resumo das vendas (em baixo da tabela de vendas)
        self.frame_resumo_vendas = ttk.Frame(self.tab_vendas)
        self.frame_resumo_vendas.pack(fill="x", padx=5, pady=5)

        self.label_total_qtd = ttk.Label(self.frame_resumo_vendas, text="Total Qtd: 0",
                                          font=("Segoe UI", 10, "bold"))
        self.label_total_qtd.pack(side="left", padx=20)

        self.label_total_vendas = ttk.Label(self.frame_resumo_vendas, text="Total Vendas: 0.00 MT",
                                             font=("Segoe UI", 10, "bold"))
        self.label_total_vendas.pack(side="left", padx=20)

        btn_registar = ttk.Button(self.frame_resumo_vendas, text="+ Registar Venda",
                                   command=self._registar_venda)
        btn_registar.pack(side="right", padx=20)

        self._actualizar_tabela_vendas()

    # ---------------- POPULAR DADOS DE EXEMPLO ----------------
    def _popular_exemplo(self):
        exemplos = [
            (1, "Pão de forma", "Pão", 80.0, 50, "15/09/2026"),
            (2, "Bolo de chocolate", "Bolo", 350.0, 10, "12/09/2026"),
            (3, "Pastel de nata", "Doce", 45.0, 30, "13/09/2026"),
            (4, "Pão careca", "Pão", 15.0, 100, "14/09/2026"),
        ]
        for e in exemplos:
            self.lista.cadastrar(*e)

        # Vendas de exemplo
        self.lista_vendas.registar_venda(1, "Pão de forma", 10, 80.0)
        self.lista_vendas.registar_venda(3, "Pastel de nata", 5, 45.0)
        self.lista_vendas.registar_venda(2, "Bolo de chocolate", 2, 350.0)

    # ---------------- actualIZAR TABELAS ----------------
    def _actualizar_tabela_registos(self, produtos=None):
        if produtos is None:
            produtos = self.lista.listar_todos()
        self.tabela_registos.delete(*self.tabela_registos.get_children())
        for p in produtos:
            self.tabela_registos.insert("", "end", values=(
                p.codigo, p.nome, p.categoria, p.preco, p.quantidade, p.validade
            ))

    def _actualizar_tabela_vendas(self):
        vendas = self.lista_vendas.listar_todas()
        self.tabela_vendas.delete(*self.tabela_vendas.get_children())
        for v in vendas:
            self.tabela_vendas.insert("", "end", values=(
                v.data, v.codigo_produto, v.nome_produto,
                v.quantidade, f"{v.preco_unitario:.2f}", f"{v.total:.2f}"
            ))
        self.label_total_qtd.config(text=f"Total Qtd: {self.lista_vendas.total_quantidade()}")
        self.label_total_vendas.config(text=f"Total Vendas: {self.lista_vendas.total_vendas():.2f} MT")

    # ---------------- LEITURA DO FORMULÁRIO ----------------
    def _ler_formulario(self):
        return {a: self.entradas[a].get().strip() for a in self.ATRIBUTOS}

    def _limpar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def _preencher_formulario(self, produto):
        self._limpar_formulario()
        self.entradas["codigo"].insert(0, str(produto.codigo))
        self.entradas["nome"].insert(0, produto.nome)
        self.entradas["categoria"].insert(0, produto.categoria)
        self.entradas["preco"].insert(0, str(produto.preco))
        self.entradas["quantidade"].insert(0, str(produto.quantidade))
        self.entradas["validade"].insert(0, produto.validade)

    # ---------------- VERIFICAÇÃO DE PERMISSÃO ----------------
    def _exige_dono(self):
        """Bloqueia a ação se o utilizador autenticado não for o Dono da Padaria."""
        if not self.e_dono:
            messagebox.showwarning(
                "Acesso restrito",
                "Esta operação está reservada ao Dono da Padaria."
            )
            return True
        return False

    # ---------------- AÇÕES DOS BOTÕES ----------------
    def acao_buscar_produto(self):
        """Abre formulário para buscar produto por código e mostrar seus dados."""
        janela = tk.Toplevel(self.root)
        janela.title("Buscar Produto")
        janela.geometry("350x120")
        janela.resizable(False, False)

        ttk.Label(janela, text="Código do Produto:").grid(row=0, column=0, padx=10, pady=15)
        entrada_codigo = ttk.Entry(janela, width=20)
        entrada_codigo.grid(row=0, column=1, padx=10, pady=15)
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

            self._preencher_formulario(produto)
            self._actualizar_tabela_registos([produto])
            janela.destroy()

        entrada_codigo.bind("<Return>", lambda e: buscar())

        ttk.Button(janela, text="Buscar", command=buscar).grid(row=1, column=0, columnspan=2, pady=5)
        janela.grab_set()

    def acao_cadastrar(self):
        if self._exige_dono():
            return
        dados = self._ler_formulario()
        try:
            codigo = int(dados["codigo"])
            preco = float(dados["preco"])
            quantidade = int(dados["quantidade"])
            self.lista.cadastrar(codigo, dados["nome"], dados["categoria"],
                                  preco, quantidade, dados["validade"])
            self._actualizar_tabela_registos()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
            self._limpar_formulario()
        except ValueError as e:
            messagebox.showerror("Erro", str(e) if str(e) else "Verifique os campos numéricos (código, preço, quantidade).")

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
        janela = tk.Toplevel(self.root)
        janela.title("Buscar por 2 atributos")

        ttk.Label(janela, text="Atributo 1:").grid(row=0, column=0, padx=5, pady=5)
        combo1 = ttk.Combobox(janela, values=self.ATRIBUTOS, state="readonly")
        combo1.grid(row=0, column=1, padx=5, pady=5)
        entrada1 = ttk.Entry(janela)
        entrada1.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(janela, text="Atributo 2:").grid(row=1, column=0, padx=5, pady=5)
        combo2 = ttk.Combobox(janela, values=self.ATRIBUTOS, state="readonly")
        combo2.grid(row=1, column=1, padx=5, pady=5)
        entrada2 = ttk.Entry(janela)
        entrada2.grid(row=1, column=2, padx=5, pady=5)

        def confirmar():
            resultados = self.lista.buscar_por_dois_atributos(
                combo1.get(), entrada1.get(), combo2.get(), entrada2.get()
            )
            self._actualizar_tabela_registos(resultados)
            self.abas.select(self.tab_registos)
            if not resultados:
                messagebox.showinfo("Busca", "Nenhum produto encontrado.")
            janela.destroy()

        ttk.Button(janela, text="Buscar", command=confirmar).grid(row=2, column=0, columnspan=3, pady=10)

    def acao_alterar(self):
        if self._exige_dono():
            return
        dados = self._ler_formulario()
        if not dados["codigo"]:
            messagebox.showwarning("Aviso", "Indique o código do produto a alterar.")
            return
        try:
            codigo = int(dados["codigo"])
            novos_dados = {
                "nome": dados["nome"],
                "categoria": dados["categoria"],
                "preco": float(dados["preco"]) if dados["preco"] else None,
                "quantidade": int(dados["quantidade"]) if dados["quantidade"] else None,
                "validade": dados["validade"],
            }
            self.lista.alterar_por_codigo(codigo, novos_dados)
            self._actualizar_tabela_registos()
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso.")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

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
        janela = tk.Toplevel(self.root)
        janela.title("Listar ordenado")

        ttk.Label(janela, text="Ordenar por:").grid(row=0, column=0, padx=5, pady=5)
        combo = ttk.Combobox(janela, values=self.ATRIBUTOS, state="readonly")
        combo.grid(row=0, column=1, padx=5, pady=5)

        decrescente_var = tk.BooleanVar()
        ttk.Checkbutton(janela, text="Ordem decrescente", variable=decrescente_var).grid(
            row=1, column=0, columnspan=2, pady=5
        )

        def confirmar():
            resultados = self.lista.listar_ordenado(combo.get(), decrescente_var.get())
            self._actualizar_tabela_registos(resultados)
            self.abas.select(self.tab_registos)
            janela.destroy()

        ttk.Button(janela, text="Ordenar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

    # ---------------- REGISTAR VENDA (a partir da aba de vendas) ----------------
    def _registar_venda(self):
        janela = tk.Toplevel(self.root)
        janela.title("Registar Venda")
        janela.geometry("400x200")
        janela.resizable(False, False)

        ttk.Label(janela, text="Código do Produto:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entrada_codigo = ttk.Entry(janela, width=25)
        entrada_codigo.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(janela, text="Quantidade:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entrada_qtd = ttk.Entry(janela, width=25)
        entrada_qtd.grid(row=1, column=1, padx=10, pady=10)

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

            produto.quantidade -= qtd
            self.lista_vendas.registar_venda(codigo, produto.nome, qtd, produto.preco)
            self._actualizar_tabela_registos()
            self._actualizar_tabela_vendas()
            messagebox.showinfo("Sucesso",
                f"Venda registada: {qtd}x {produto.nome} = {qtd * produto.preco:.2f} MT", parent=janela)
            janela.destroy()

        ttk.Button(janela, text="Registar Venda", command=confirmar).grid(
            row=2, column=0, columnspan=2, pady=15)
        janela.grab_set()

    # ---------------- JANELAS AUXILIARES ----------------
    def _pedir_atributo_valor(self, titulo):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        resultado = {"atributo": None, "valor": None}

        ttk.Label(janela, text="Atributo:").grid(row=0, column=0, padx=5, pady=5)
        combo = ttk.Combobox(janela, values=self.ATRIBUTOS, state="readonly")
        combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(janela, text="Valor:").grid(row=1, column=0, padx=5, pady=5)
        entrada = ttk.Entry(janela)
        entrada.grid(row=1, column=1, padx=5, pady=5)

        def confirmar():
            resultado["atributo"] = combo.get()
            resultado["valor"] = entrada.get()
            janela.destroy()

        ttk.Button(janela, text="Confirmar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)
        janela.grab_set()
        self.root.wait_window(janela)

        return resultado["atributo"], resultado["valor"]

    def _pedir_valor_simples(self, titulo, label_texto):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        resultado = {"valor": None}

        ttk.Label(janela, text=label_texto).grid(row=0, column=0, padx=5, pady=5)
        entrada = ttk.Entry(janela)
        entrada.grid(row=0, column=1, padx=5, pady=5)

        def confirmar():
            resultado["valor"] = entrada.get()
            janela.destroy()

        ttk.Button(janela, text="Confirmar", command=confirmar).grid(row=1, column=0, columnspan=2, pady=10)
        janela.grab_set()
        self.root.wait_window(janela)

        return resultado["valor"]
