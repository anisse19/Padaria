"""Tela inicial (splash): nome do sistema sobre uma imagem de fundo."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

CAMINHO_IMAGEM_FUNDO = Path(__file__).resolve().parents[2] / "assets" / "imagens" / "fundo.png"


class TelaInicial:
    """Primeira tela mostrada ao abrir o programa: nome do sistema sobre uma
    imagem de fundo, com um botão 'Acessar' que leva à tela de login."""

    LARGURA = 640
    ALTURA_IMAGEM = 320
    ALTURA_RODAPE = 90

    def __init__(self, root, ao_acessar):
        self.root = root
        self.ao_acessar = ao_acessar

        self.root.title("Padaria Adonai")
        self.root.geometry(f"{self.LARGURA}x{self.ALTURA_IMAGEM + self.ALTURA_RODAPE}")
        self.root.resizable(False, False)

        # A imagem precisa de ser guardada como atributo, senão o Python
        # recolhe o lixo e ela desaparece do ecrã.
        self.imagem_fundo = tk.PhotoImage(file=CAMINHO_IMAGEM_FUNDO)

        canvas = tk.Canvas(
            self.root,
            width=self.LARGURA,
            height=self.ALTURA_IMAGEM,
            highlightthickness=0,
        )
        canvas.pack(side="top", fill="x")
        canvas.create_image(0, 0, anchor="nw", image=self.imagem_fundo)
        canvas.create_text(
            self.LARGURA // 2, self.ALTURA_IMAGEM // 2,
            text="Sistema de Gestão\nPadaria Adonai",
            font=("Segoe UI", 24, "bold"),
            fill="white",
            justify="center",
        )

        rodape = tk.Frame(self.root, bg="#2b2320", height=self.ALTURA_RODAPE)
        rodape.pack(side="bottom", fill="both", expand=True)
        rodape.pack_propagate(False)

        estilo = ttk.Style()
        estilo.configure("Acessar.TButton", font=("Segoe UI", 12, "bold"), padding=8)

        btn_acessar = ttk.Button(
            rodape, text="Acessar", style="Acessar.TButton",
            command=self._acessar,
        )
        btn_acessar.place(relx=0.5, rely=0.5, anchor="center", width=180)

    def _acessar(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.ao_acessar()
