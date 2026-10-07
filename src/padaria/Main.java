package padaria;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import padaria.telas.AplicacaoPadaria;
import padaria.telas.Tema;
import padaria.telas.TelaInicial;
import padaria.telas.TelaLogin;

/**
 * Ponto de entrada e fluxo dos ecrãs: Tela inicial -> Login -> Aplicação principal.
 *
 * Os ecrãs não se conhecem: cada um recebe um callback que chama quando
 * termina. Para mudar o fluxo, só se mexe neste ficheiro.
 */
public class Main {

	public static void main(String[] args) {
		Tema.aplicar();
		SwingUtilities.invokeLater(Main::novaSessao);
	}

	/** Abre uma janela nova na tela inicial. Usado no arranque e no botão "Sair". */
	private static void novaSessao() {
		final JFrame root = new JFrame();
		// Fechar a janela termina o programa (não há mais janelas abertas).
		root.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

		TelaLogin.AoAutenticar aoAutenticar = perfil -> new AplicacaoPadaria(root, perfil, Main::novaSessao);
		Runnable aoAcessar = () -> new TelaLogin(root, aoAutenticar);
		new TelaInicial(root, aoAcessar);

		root.setVisible(true);
	}
}
