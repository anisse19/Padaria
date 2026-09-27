"""Ecrã de login com controlo de acesso."""

import tkinter as tk
from tkinter import ttk

from src.config import NOME_PADARIA, UTILIZADORES
from src.interface.tema import centrar_janela


class TelaLogin:
    """Em caso de sucesso chama ao_autenticar(registo), com o dicionário do
    utilizador em UTILIZADORES. É esse o `perfil` da AplicacaoPadaria."""

    LARGURA = 420
    ALTURA = 480

    def __init__(self, root, ao_autenticar):
        self.root = root
        self.ao_autenticar = ao_autenticar

        self.root.title(f"{NOME_PADARIA} - Login")
        centrar_janela(self.root, self.LARGURA, self.ALTURA)
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=(40, 30))
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="🥐", style="Logo.TLabel").pack()
        ttk.Label(frame, text=NOME_PADARIA, style="Titulo.TLabel").pack()
        ttk.Label(frame, text="Bem-vindo(a) de volta ao forno",
                  style="Subtitulo.TLabel").pack(pady=(0, 25))

        ttk.Label(frame, text="Utilizador").pack(anchor="w")
        self.entrada_utilizador = ttk.Entry(frame)
        self.entrada_utilizador.pack(fill="x", pady=(2, 12))

        ttk.Label(frame, text="Senha").pack(anchor="w")
        self.entrada_senha = ttk.Entry(frame, show="•")
        self.entrada_senha.pack(fill="x", pady=(2, 8))

        self.label_erro = ttk.Label(frame, text="", style="Erro.TLabel")
        self.label_erro.pack(pady=(0, 8))

        ttk.Button(frame, text="Entrar", command=self._tentar_login).pack(fill="x")

        self.entrada_utilizador.focus()
        self.entrada_senha.bind("<Return>", lambda e: self._tentar_login())
        self.entrada_utilizador.bind("<Return>", lambda e: self.entrada_senha.focus())

    def _tentar_login(self):
        utilizador = self.entrada_utilizador.get().strip()
        senha = self.entrada_senha.get()

        registo = UTILIZADORES.get(utilizador)
        # Mensagem genérica: não revela se o erro foi no utilizador ou na senha.
        if registo is None or registo["senha"] != senha:
            self.label_erro.config(text="Utilizador ou senha inválidos.")
            self.entrada_senha.delete(0, tk.END)
            return

        for widget in self.root.winfo_children():
            widget.destroy()
        self.ao_autenticar(registo)
