package principal;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import listas_duplamente_ligadas.AplicacaoPadaria;
import listas_duplamente_ligadas.SistemaPadaria;
import listas_duplamente_ligadas.TelaInicial;
import listas_duplamente_ligadas.TelaLogin;

/**
 * Ponto de entrada: é esta a classe que se corre para abrir o programa.
 *
 * Fluxo dos ecrãs: Tela inicial -> Login -> Aplicação principal. Os ecrãs não
 * se conhecem: cada um recebe um callback que chama quando termina. Para mudar
 * o fluxo, só se mexe em novaSessao().
 */
public class Main {

	public static void main(String[] args) {
		SistemaPadaria.aplicarTema();
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
