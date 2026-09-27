"""Fluxo dos ecrãs: Tela inicial -> Login -> Aplicação principal.

Os ecrãs não se conhecem: cada um recebe um callback que chama quando
termina. Para mudar o fluxo, só se mexe neste ficheiro.
"""

import tkinter as tk

from src.interface import AplicacaoPadaria, TelaInicial, TelaLogin
from src.interface.tema import aplicar_tema


def criar_janela_raiz():
    """Usar sempre em vez de tk.Tk(), para a janela nova já ter o tema."""
    root = tk.Tk()
    aplicar_tema(root)
    return root


def iniciar_aplicacao(root):
    def ao_autenticar(perfil):
        AplicacaoPadaria(root, perfil, ao_terminar_sessao)

    def ao_acessar():
        TelaLogin(root, ao_autenticar)

    TelaInicial(root, ao_acessar)


def ao_terminar_sessao():
    """Botão 'Sair': recomeça numa janela nova. Os dados da sessão perdem-se,
    porque vivem dentro de AplicacaoPadaria."""
    iniciar_aplicacao(criar_janela_raiz())


def main():
    root = criar_janela_raiz()
    iniciar_aplicacao(root)
    root.mainloop()  # corre enquanto houver alguma janela Tk aberta
