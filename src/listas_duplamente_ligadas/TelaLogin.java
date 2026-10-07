package listas_duplamente_ligadas;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;


/** Ecrã de login com controlo de acesso. */
public class TelaLogin {

	/** Chamado com o utilizador autenticado. É esse o "perfil" da AplicacaoPadaria. */
	public interface AoAutenticar {
		void autenticado(Utilizador utilizador);
	}

	private static final int LARGURA = 420;
	private static final int ALTURA = 460;

	private final AoAutenticar aoAutenticar;
	private final JTextField entradaUtilizador = new JTextField();
	private final JPasswordField entradaSenha = new JPasswordField();
	private final JLabel labelErro = SistemaPadaria.rotulo(" ", SistemaPadaria.FONTE_PEQUENA, SistemaPadaria.ERRO);

	public TelaLogin(JFrame janela, AoAutenticar aoAutenticar) {
		this.aoAutenticar = aoAutenticar;

		janela.setTitle(SistemaPadaria.NOME_PADARIA + " - Login");

		JPanel frame = new JPanel();
		frame.setLayout(new BoxLayout(frame, BoxLayout.Y_AXIS));
		frame.setBorder(BorderFactory.createEmptyBorder(30, 40, 30, 40));

		adicionar(frame, SistemaPadaria.rotulo(SistemaPadaria.NOME_PADARIA, SistemaPadaria.FONTE_TITULO, SistemaPadaria.CROSTA), true);
		adicionar(frame, SistemaPadaria.rotulo("Bem-vindo(a) de volta ao forno", SistemaPadaria.FONTE_SUBTITULO, SistemaPadaria.TEXTO_SUAVE), true);
		frame.add(Box.createVerticalStrut(30));

		adicionar(frame, new JLabel("Utilizador"), false);
		adicionar(frame, campo(entradaUtilizador), false);
		frame.add(Box.createVerticalStrut(12));

		adicionar(frame, new JLabel("Senha"), false);
		adicionar(frame, campo(entradaSenha), false);
		frame.add(Box.createVerticalStrut(8));

		adicionar(frame, labelErro, true);
		frame.add(Box.createVerticalStrut(8));

		JButton btnEntrar = SistemaPadaria.botao("Entrar");
		btnEntrar.setMaximumSize(new Dimension(Integer.MAX_VALUE, 40));
		adicionar(frame, btnEntrar, false);

		ActionListener tentarLogin = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				tentarLogin();
			}
		};
		btnEntrar.addActionListener(tentarLogin);
		entradaSenha.addActionListener(tentarLogin);  // Enter na senha
		entradaUtilizador.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				entradaSenha.requestFocusInWindow();  // Enter no utilizador passa à senha
			}
		});

		janela.setContentPane(frame);
		janela.getRootPane().setDefaultButton(null);  // o Enter é tratado nos campos
		janela.setMinimumSize(null);
		janela.setSize(LARGURA, ALTURA);
		janela.setResizable(false);
		SistemaPadaria.centrarJanela(janela);
		janela.revalidate();
		entradaUtilizador.requestFocusInWindow();
	}

	private void tentarLogin() {
		String utilizador = entradaUtilizador.getText().trim();
		String senha = new String(entradaSenha.getPassword());

		Utilizador registo = SistemaPadaria.UTILIZADORES.get(utilizador);
		// Mensagem genérica: não revela se o erro foi no utilizador ou na senha.
		if (registo == null || !registo.senhaCorrecta(senha)) {
			labelErro.setText("Utilizador ou senha inválidos.");
			entradaSenha.setText("");
			return;
		}
		aoAutenticar.autenticado(registo);
	}

	private static JTextField campo(JTextField campo) {
		campo.setBackground(SistemaPadaria.BRANCO);
		campo.setForeground(SistemaPadaria.TEXTO);
		campo.setBorder(BorderFactory.createCompoundBorder(
				BorderFactory.createLineBorder(SistemaPadaria.PAINEL, 2),
				BorderFactory.createEmptyBorder(5, 5, 5, 5)));
		campo.setMaximumSize(new Dimension(Integer.MAX_VALUE, campo.getPreferredSize().height));
		return campo;
	}

	/**
	 * Num BoxLayout todos os filhos ficam alinhados à esquerda; os textos
	 * "centrados" ocupam a largura toda e centram o próprio texto.
	 */
	private static void adicionar(JPanel painel, JComponent componente, boolean centrado) {
		componente.setAlignmentX(Component.LEFT_ALIGNMENT);
		if (centrado && componente instanceof JLabel) {
			((JLabel) componente).setHorizontalAlignment(JLabel.CENTER);
			componente.setMaximumSize(new Dimension(Integer.MAX_VALUE, componente.getPreferredSize().height));
		}
		painel.add(componente);
	}
}
