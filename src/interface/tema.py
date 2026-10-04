"""Tema visual: cores quentes de padaria.

Todas as cores e fontes vivem aqui, e os outros ficheiros usam CORES[...] e
FONTE_*. Estilos ttk: "Nome.Base" (ex.: "Sidebar.TButton") herda da base;
configure() define o aspeto normal, e map() o aspeto por estado
("active" = rato por cima).
"""

from tkinter import ttk

CORES = {
    "fundo":         "#FBF3E4",  # miolo do pão
    "painel":        "#F3E1C7",  # massa: barra de topo, linhas alternadas
    "crosta":        "#8B5A2B",  # sidebar, cabeçalhos, títulos
    "crosta_escura": "#5C3A1E",  # hover, rodapé da tela inicial
    "dourado":       "#D9A441",  # botões e seleção
    "dourado_claro": "#EBC77A",  # hover dos botões
    "texto":         "#3E2A1E",  # chocolate
    "texto_suave":   "#7A6555",
    "branco":        "#FFFDF8",  # campos de texto e tabelas
    "erro":          "#B3261E",
}

# Georgia e Helvetica existem no macOS e no Windows (ao contrário de Segoe UI).
FONTE_TITULO = ("Georgia", 22, "bold")
FONTE_SUBTITULO = ("Georgia", 14, "italic")
FONTE_SECCAO = ("Georgia", 14, "bold")
FONTE_NORMAL = ("Helvetica", 12)
FONTE_NEGRITO = ("Helvetica", 12, "bold")
FONTE_PEQUENA = ("Helvetica", 11)


def aplicar_tema(root):
    """Chamar uma vez por cada tk.Tk(): os estilos pertencem a cada janela raiz."""
    root.configure(bg=CORES["fundo"])
    root.option_add("*Toplevel.background", CORES["fundo"])
    # A lista suspensa da Combobox é um widget tk clássico: configura-se assim.
    root.option_add("*TCombobox*Listbox.background", CORES["branco"])
    root.option_add("*TCombobox*Listbox.foreground", CORES["texto"])
    root.option_add("*TCombobox*Listbox.selectBackground", CORES["dourado"])
    root.option_add("*TCombobox*Listbox.font", FONTE_NORMAL)

    estilo = ttk.Style(root)
    # O tema do macOS ("aqua") ignora as cores dos botões; o "clam" respeita-as.
    estilo.theme_use("clam")

    estilo.configure(
        ".",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=FONTE_NORMAL,
        bordercolor=CORES["painel"],
        lightcolor=CORES["fundo"],
        darkcolor=CORES["painel"],
        focuscolor=CORES["dourado"],
    )

    # --- Textos ---
    estilo.configure("Titulo.TLabel", font=FONTE_TITULO, foreground=CORES["crosta"])
    estilo.configure("Subtitulo.TLabel", font=FONTE_SUBTITULO, foreground=CORES["texto_suave"])
    estilo.configure("Seccao.TLabel", font=FONTE_SECCAO, foreground=CORES["crosta"])
    estilo.configure("Suave.TLabel", font=FONTE_PEQUENA, foreground=CORES["texto_suave"])
    estilo.configure("Erro.TLabel", font=FONTE_PEQUENA, foreground=CORES["erro"])
    estilo.configure("Resumo.TLabel", font=FONTE_NEGRITO, foreground=CORES["crosta"])
    estilo.configure("Logo.TLabel", font=("Helvetica", 48))

    # --- Botões ---
    estilo.configure("TButton", background=CORES["dourado"], foreground=CORES["texto"],
                     font=FONTE_NEGRITO, borderwidth=0, padding=(14, 8))
    estilo.map("TButton",
               background=[("pressed", CORES["crosta"]), ("active", CORES["dourado_claro"])])

    estilo.configure("Secundario.TButton", background=CORES["crosta"],
                     foreground=CORES["branco"], padding=(16, 6))
    estilo.map("Secundario.TButton",
               background=[("pressed", CORES["crosta_escura"]), ("active", CORES["crosta_escura"])])

    estilo.configure("Acessar.TButton", font=("Helvetica", 14, "bold"), padding=(20, 10))

    # --- Barra de topo ---
    estilo.configure("Topo.TFrame", background=CORES["painel"])
    estilo.configure("Topo.TLabel", background=CORES["painel"])
    estilo.configure("TopoMarca.TLabel", background=CORES["painel"],
                     foreground=CORES["crosta"], font=FONTE_SECCAO)
    estilo.configure("TopoSuave.TLabel", background=CORES["painel"],
                     foreground=CORES["texto_suave"], font=FONTE_PEQUENA)

    # --- Sidebar ---
    estilo.configure("Sidebar.TFrame", background=CORES["crosta"])
    estilo.configure("Sidebar.TLabel", background=CORES["crosta"],
                     foreground=CORES["branco"], font=FONTE_SECCAO)
    estilo.configure("Sidebar.TButton", background=CORES["crosta"], foreground=CORES["branco"],
                     font=FONTE_NORMAL, anchor="w", padding=(12, 7))
    estilo.map("Sidebar.TButton",
               background=[("pressed", CORES["crosta_escura"]), ("active", CORES["dourado"])],
               foreground=[("active", CORES["texto"])])

    # --- Campos ---
    for base in ("TEntry", "TCombobox"):
        estilo.configure(base, fieldbackground=CORES["branco"], padding=5,
                         bordercolor=CORES["painel"], lightcolor=CORES["branco"])
        estilo.map(base, bordercolor=[("focus", CORES["dourado"])],
                   lightcolor=[("focus", CORES["dourado"])])
    estilo.map("TCombobox", fieldbackground=[("readonly", CORES["branco"])])
    # Campo só de leitura (ex.: código na janela Alterar).
    estilo.map("TEntry", fieldbackground=[("disabled", CORES["painel"])],
               foreground=[("disabled", CORES["texto_suave"])])

    estilo.configure("TCheckbutton", background=CORES["fundo"])
    estilo.map("TCheckbutton", background=[("active", CORES["fundo"])],
               indicatorcolor=[("selected", CORES["dourado"])])

    # --- Abas ---
    estilo.configure("TNotebook", background=CORES["fundo"], borderwidth=0)
    estilo.configure("TNotebook.Tab", background=CORES["painel"], padding=(16, 6),
                     font=FONTE_NEGRITO)
    estilo.map("TNotebook.Tab",
               background=[("selected", CORES["dourado"])],
               expand=[("selected", (1, 1, 1, 0))])

    # --- Tabelas ---
    estilo.configure("Treeview", background=CORES["branco"], fieldbackground=CORES["branco"],
                     foreground=CORES["texto"], rowheight=30, borderwidth=0)
    estilo.map("Treeview",
               background=[("selected", CORES["dourado"])],
               foreground=[("selected", CORES["texto"])])
    estilo.configure("Treeview.Heading", background=CORES["crosta"],
                     foreground=CORES["branco"], font=FONTE_NEGRITO, padding=6)
    estilo.map("Treeview.Heading", background=[("active", CORES["crosta_escura"])])

    estilo.configure("Vertical.TScrollbar", background=CORES["painel"],
                     troughcolor=CORES["fundo"], arrowcolor=CORES["crosta"])


def configurar_linhas_alternadas(tabela):
    """Linhas inseridas com tags=("par",) ficam com fundo alternado."""
    tabela.tag_configure("par", background=CORES["painel"])


def centrar_janela(janela, largura=None, altura=None):
    """Centra a janela no ecrã. Sem tamanho, usa o que o conteúdo pede, por
    isso nesse caso deve ser chamada depois de criar os widgets."""
    janela.update_idletasks()
    largura = largura or janela.winfo_reqwidth()
    altura = altura or janela.winfo_reqheight()
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 3 
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
