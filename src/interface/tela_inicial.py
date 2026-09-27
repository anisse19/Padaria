"""Tela inicial (splash): nome da padaria sobre uma imagem de fundo."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from src.config import NOME_PADARIA
from src.interface.tema import CORES, centrar_janela

# Relativo a este ficheiro, para funcionar seja qual for a pasta de onde se corre.
CAMINHO_IMAGEM_FUNDO = Path(__file__).resolve().parents[2] / "assets" / "imagens" / "fundo.png"


class TelaInicial:
    """Imagem de fundo com o nome da padaria e um botão 'Acessar'."""

    # Têm de coincidir com o tamanho do PNG (o PhotoImage não redimensiona).
    LARGURA = 640
    ALTURA_IMAGEM = 320
    ALTURA_RODAPE = 90

    def __init__(self, root, ao_acessar):
        self.root = root
        self.ao_acessar = ao_acessar

        self.root.title(NOME_PADARIA)
        centrar_janela(self.root, self.LARGURA, self.ALTURA_IMAGEM + self.ALTURA_RODAPE)
        self.root.resizable(True, True)
        # Nunca mais pequena do que a imagem + rodapé, para não cortar nada.
        self.root.minsize(self.LARGURA, self.ALTURA_IMAGEM + self.ALTURA_RODAPE)

        # Guardada como atributo, senão o Python recolhe-a e a imagem desaparece.
        self.imagem_fundo = tk.PhotoImage(file=CAMINHO_IMAGEM_FUNDO)

        # O rodapé é empacotado primeiro, para ficar sempre em baixo com altura
        # fixa; o canvas ocupa todo o espaço que sobra.
        rodape = tk.Frame(self.root, bg=CORES["crosta_escura"], height=self.ALTURA_RODAPE)
        rodape.pack(side="bottom", fill="x")
        rodape.pack_propagate(False)

        # Fundo escuro: quando a janela é maior do que a imagem, a margem à
        # volta tem a mesma cor do rodapé.
        self.canvas = tk.Canvas(
            self.root,
            width=self.LARGURA,
            height=self.ALTURA_IMAGEM,
            highlightthickness=0,
            bg=CORES["crosta_escura"],
        )
        self.canvas.pack(side="top", fill="both", expand=True)
        # <Configure> dispara sempre que o canvas muda de tamanho.
        self.canvas.bind("<Configure>", self._desenhar)

        btn_acessar = ttk.Button(
            rodape, text="Acessar", style="Acessar.TButton",
            command=self._acessar,
        )
        btn_acessar.place(relx=0.5, rely=0.5, anchor="center", width=200)
        btn_acessar.focus()
        self.root.bind("<Return>", lambda e: self._acessar())

    def _desenhar(self, evento):
        """Redesenha a imagem e os textos no centro do canvas.
        O PhotoImage não redimensiona, por isso a imagem fica centrada no tamanho original."""
        self.canvas.delete("all")
        centro_x = evento.width // 2
        centro_y = evento.height // 2
        self.canvas.create_image(centro_x, centro_y, anchor="center", image=self.imagem_fundo)
        self._texto_com_sombra(self.canvas, centro_x, centro_y - 30, "🥖", ("Helvetica", 40))
        self._texto_com_sombra(self.canvas, centro_x, centro_y + 25, NOME_PADARIA,
                               ("Georgia", 32, "bold"))
        self._texto_com_sombra(self.canvas, centro_x, centro_y + 70,
                               "Pão quentinho, feito com carinho",
                               ("Georgia", 15, "italic"))

    @staticmethod
    def _texto_com_sombra(canvas, x, y, texto, fonte):
        """Sombra escura deslocada 2px, para o texto se ler sobre qualquer imagem."""
        canvas.create_text(x + 2, y + 2, text=texto, font=fonte,
                           fill=CORES["crosta_escura"], justify="center")
        canvas.create_text(x, y, text=texto, font=fonte,
                           fill=CORES["branco"], justify="center")

    def _acessar(self):
        self.root.unbind("<Return>")  # senão o Enter do login voltava a chamar isto
        self.root.minsize(1, 1)       # o login é mais estreito do que este mínimo
        for widget in self.root.winfo_children():
            widget.destroy()
        self.ao_acessar()
