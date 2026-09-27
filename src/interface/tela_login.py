"""Ecrã de login com controlo de acesso."""

import tkinter as tk
from tkinter import ttk

from src.config import UTILIZADORES


class TelaLogin:
    """Janela inicial de autenticação. Só avança para o sistema quem tiver
    utilizador e senha correspondentes a um registo em UTILIZADORES."""

    def __init__(self, root, ao_autenticar):
        self.root = root
        self.ao_autenticar = ao_autenticar

        self.root.title("Padaria - Login")
        self.root.geometry("380x260")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Sistema de Gestão de Padaria",
                  font=("Segoe UI", 13, "bold")).pack(pady=(0, 15))

        ttk.Label(frame, text="Utilizador:").pack(anchor="w")
        self.entrada_utilizador = ttk.Entry(frame)
        self.entrada_utilizador.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.entrada_senha = ttk.Entry(frame, show="*")
        self.entrada_senha.pack(fill="x", pady=(0, 15))

        self.label_erro = ttk.Label(frame, text="", foreground="red")
        self.label_erro.pack(pady=(0, 5))

        btn = ttk.Button(frame, text="Entrar", command=self._tentar_login)
        btn.pack(fill="x")

        self.entrada_utilizador.focus()
        self.entrada_senha.bind("<Return>", lambda e: self._tentar_login())
        self.entrada_utilizador.bind("<Return>", lambda e: self.entrada_senha.focus())

    def _tentar_login(self):
        utilizador = self.entrada_utilizador.get().strip()
        senha = self.entrada_senha.get()

        registo = UTILIZADORES.get(utilizador)
        if registo is None or registo["senha"] != senha:
            self.label_erro.config(text="Utilizador ou senha inválidos.")
            self.entrada_senha.delete(0, tk.END)
            return

        # Autenticado: limpa a janela e entrega o controlo à aplicação principal
        for widget in self.root.winfo_children():
            widget.destroy()
        self.ao_autenticar(registo)
