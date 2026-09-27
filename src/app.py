"""Liga os ecrãs entre si: Tela inicial -> Login -> Aplicação principal."""

import tkinter as tk

from src.interface import AplicacaoPadaria, TelaInicial, TelaLogin


def iniciar_aplicacao(root):
    """Mostra a tela inicial; ao clicar em 'Acessar' vai para o login;
    só depois de autenticado é que o sistema principal é aberto."""

    def ao_autenticar(perfil):
        AplicacaoPadaria(root, perfil, ao_terminar_sessao)

    def ao_acessar():
        TelaLogin(root, ao_autenticar)

    TelaInicial(root, ao_acessar)


def ao_terminar_sessao():
    """Chamado quando o utilizador clica em 'Sair': abre uma janela nova
    e recomeça pela tela inicial."""
    nova_janela = tk.Tk()
    iniciar_aplicacao(nova_janela)


def main():
    root = tk.Tk()
    iniciar_aplicacao(root)
    root.mainloop()
