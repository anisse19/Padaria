package padaria.telas;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagLayout;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

import padaria.Config;

/** Tela inicial (splash): nome da padaria sobre uma imagem de fundo e um botão "Acessar". */
public class TelaInicial {

	// Relativo à pasta do projecto (é a pasta de trabalho no Eclipse e no "java -cp bin").
	private static final String CAMINHO_IMAGEM_FUNDO = "assets/imagens/fundo.png";

	private static final int LARGURA = 640;
	private static final int ALTURA_IMAGEM = 320;
	private static final int ALTURA_RODAPE = 90;

	public TelaInicial(final JFrame janela, final Runnable aoAcessar) {
		janela.setTitle(Config.NOME_PADARIA);

		final BufferedImage imagemFundo = carregarImagem();

		// O canvas ocupa o espaço que sobra; a imagem fica centrada no tamanho original.
		JPanel canvas = new JPanel() {
			@Override
			protected void paintComponent(Graphics g) {
				super.paintComponent(g);
				Graphics2D g2 = (Graphics2D) g;
				g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
				int centroX = getWidth() / 2;
				int centroY = getHeight() / 2;
				if (imagemFundo != null) {
					g2.drawImage(imagemFundo, centroX - imagemFundo.getWidth() / 2,
							centroY - imagemFundo.getHeight() / 2, null);
				}
				textoComSombra(g2, centroX, centroY + 10, Config.NOME_PADARIA, new Font("Georgia", Font.BOLD, 36));
				textoComSombra(g2, centroX, centroY + 55, "Pão quentinho, feito com carinho",
						new Font("Georgia", Font.ITALIC, 18));
			}
		};
		// Fundo escuro: quando a janela é maior do que a imagem, a margem tem a cor do rodapé.
		canvas.setBackground(Tema.CROSTA_ESCURA);
		canvas.setPreferredSize(new Dimension(LARGURA, ALTURA_IMAGEM));

		JPanel rodape = new JPanel(new GridBagLayout());  // GridBag sem restrições = centrado
		rodape.setBackground(Tema.CROSTA_ESCURA);
		rodape.setPreferredSize(new Dimension(LARGURA, ALTURA_RODAPE));

		JButton btnAcessar = Tema.botao("Acessar");
		btnAcessar.setFont(new Font("SansSerif", Font.BOLD, 16));
		btnAcessar.setPreferredSize(new Dimension(200, 44));
		btnAcessar.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				aoAcessar.run();
			}
		});
		rodape.add(btnAcessar);

		JPanel conteudo = new JPanel(new BorderLayout());
		conteudo.add(canvas, BorderLayout.CENTER);
		conteudo.add(rodape, BorderLayout.SOUTH);

		janela.setContentPane(conteudo);
		janela.getRootPane().setDefaultButton(btnAcessar);  // Enter = Acessar
		janela.setResizable(true);
		janela.pack();
		// Nunca mais pequena do que a imagem + rodapé, para não cortar nada.
		janela.setMinimumSize(janela.getSize());
		Tema.centrarJanela(janela);
		btnAcessar.requestFocusInWindow();
	}

	private static BufferedImage carregarImagem() {
		try {
			return ImageIO.read(new File(CAMINHO_IMAGEM_FUNDO));
		} catch (IOException e) {
			return null;  // sem imagem fica só o fundo castanho
		}
	}

	/** Sombra escura deslocada 2px, para o texto se ler sobre qualquer imagem. */
	private static void textoComSombra(Graphics2D g, int centroX, int y, String texto, Font fonte) {
		g.setFont(fonte);
		FontMetrics metricas = g.getFontMetrics();
		int x = centroX - metricas.stringWidth(texto) / 2;
		g.setColor(Tema.CROSTA_ESCURA);
		g.drawString(texto, x + 2, y + 2);
		g.setColor(Tema.BRANCO);
		g.drawString(texto, x, y);
	}
}
