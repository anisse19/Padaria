package listas_duplamente_ligadas;

import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.Window;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JTable;
import javax.swing.SwingConstants;
import javax.swing.UIManager;
import javax.swing.plaf.metal.MetalLookAndFeel;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.JTableHeader;

/**
 * Configuração e tema visual do sistema. O programa arranca em principal.Main.
 */
public final class SistemaPadaria {

	// ================= CONFIGURAÇÃO =================
	// Valores de negócio que podem mudar sem mexer no resto do código.

	public static final String NOME_PADARIA = "Padaria Adonai";
	public static final String MOEDA = "MT";

	// Comparar sempre com estas constantes, nunca com texto escrito à mão.
	public static final String PERFIL_DONO = "Dono da Padaria";
	public static final String PERFIL_FUNCIONARIO = "Funcionário";

	// Senhas em texto simples: aceitável só num trabalho académico.
	public static final Map<String, Utilizador> UTILIZADORES = new HashMap<String, Utilizador>();
	static {
		UTILIZADORES.put("dono", new Utilizador("dono123", PERFIL_DONO, "Proprietário(a)"));
		UTILIZADORES.put("funcionario", new Utilizador("func123", PERFIL_FUNCIONARIO, "Funcionário(a)"));
	}

	// Operações reservadas ao Dono. Têm de ser iguais ao texto dos botões em
	// AplicacaoPadaria.construirSidebar.
	public static final Set<String> OPERACOES_RESTRITAS_AO_DONO = new HashSet<String>(Arrays.asList(
			"Cadastrar",
			"Alterar (por código)",
			"Eliminar por posição",
			"Eliminar por código"));

	// ================= TEMA VISUAL =================
	// Cores quentes de padaria. Todas as cores e fontes vivem aqui; as telas
	// usam SistemaPadaria.FUNDO, SistemaPadaria.botao(...), etc.


	public static final Color FUNDO = new Color(0xFBF3E4);          // miolo do pão
	public static final Color PAINEL = new Color(0xF3E1C7);         // massa: barra de topo, linhas alternadas
	public static final Color CROSTA = new Color(0x8B5A2B);         // sidebar, cabeçalhos, títulos
	public static final Color CROSTA_ESCURA = new Color(0x5C3A1E);  // hover, rodapé da tela inicial
	public static final Color DOURADO = new Color(0xD9A441);        // botões e selecção
	public static final Color DOURADO_CLARO = new Color(0xEBC77A);  // hover dos botões
	public static final Color TEXTO = new Color(0x3E2A1E);          // chocolate
	public static final Color TEXTO_SUAVE = new Color(0x7A6555);
	public static final Color BRANCO = new Color(0xFFFDF8);         // campos de texto e tabelas
	public static final Color ERRO = new Color(0xB3261E);

	// Georgia e SansSerif existem (ou têm substituto) em todos os sistemas.
	public static final Font FONTE_TITULO = new Font("Georgia", Font.BOLD, 26);
	public static final Font FONTE_SUBTITULO = new Font("Georgia", Font.ITALIC, 16);
	public static final Font FONTE_SECCAO = new Font("Georgia", Font.BOLD, 17);
	public static final Font FONTE_NORMAL = new Font("SansSerif", Font.PLAIN, 14);
	public static final Font FONTE_NEGRITO = new Font("SansSerif", Font.BOLD, 14);
	public static final Font FONTE_PEQUENA = new Font("SansSerif", Font.PLAIN, 13);


	/** Chamar uma vez, antes de criar qualquer janela. */
	public static void aplicarTema() {
		try {
			// O "Metal" respeita as cores dos componentes em todos os sistemas
			// (o aspecto nativo do macOS/Windows ignora-as em botões).
			UIManager.setLookAndFeel(new MetalLookAndFeel());
		} catch (Exception e) {
			// Fica o aspecto por omissão; as cores continuam a ser aplicadas.
		}
		UIManager.put("Panel.background", FUNDO);
		UIManager.put("OptionPane.background", FUNDO);
		UIManager.put("OptionPane.messageFont", FONTE_NORMAL);
		UIManager.put("OptionPane.buttonFont", FONTE_NEGRITO);
		UIManager.put("Label.font", FONTE_NORMAL);
		UIManager.put("Label.foreground", TEXTO);
		UIManager.put("TextField.font", FONTE_NORMAL);
		UIManager.put("PasswordField.font", FONTE_NORMAL);
		UIManager.put("ComboBox.font", FONTE_NORMAL);
		UIManager.put("ComboBox.background", BRANCO);
		UIManager.put("ComboBox.selectionBackground", DOURADO);
		UIManager.put("CheckBox.font", FONTE_NORMAL);
		UIManager.put("CheckBox.background", FUNDO);
		UIManager.put("TabbedPane.font", FONTE_NEGRITO);
		UIManager.put("TabbedPane.selected", DOURADO);
		UIManager.put("TabbedPane.background", PAINEL);
		UIManager.put("TabbedPane.contentAreaColor", FUNDO);
		UIManager.put("Button.font", FONTE_NEGRITO);
		UIManager.put("Button.select", CROSTA);
	}

	// ---------------- BOTÕES ----------------

	/** Botão principal (dourado). */
	public static JButton botao(String texto) {
		JButton botao = botaoBase(texto, DOURADO, TEXTO, DOURADO_CLARO, TEXTO);
		botao.setFont(FONTE_NEGRITO);
		botao.setBorder(BorderFactory.createEmptyBorder(8, 14, 8, 14));
		return botao;
	}

	/** Botão secundário (castanho), ex.: "Sair". */
	public static JButton botaoSecundario(String texto) {
		JButton botao = botaoBase(texto, CROSTA, BRANCO, CROSTA_ESCURA, BRANCO);
		botao.setFont(FONTE_NEGRITO);
		botao.setBorder(BorderFactory.createEmptyBorder(6, 16, 6, 16));
		return botao;
	}

	/** Botão da barra lateral: alinhado à esquerda, fica dourado com o rato por cima. */
	public static JButton botaoSidebar(String texto) {
		JButton botao = botaoBase(texto, CROSTA, BRANCO, DOURADO, TEXTO);
		botao.setFont(FONTE_NORMAL);
		botao.setHorizontalAlignment(SwingConstants.LEFT);
		botao.setBorder(BorderFactory.createEmptyBorder(7, 12, 7, 12));
		return botao;
	}

	private static JButton botaoBase(String texto, final Color fundo, final Color frente,
			final Color fundoHover, final Color frenteHover) {
		final JButton botao = new JButton(texto);
		botao.setBackground(fundo);
		botao.setForeground(frente);
		botao.setOpaque(true);
		botao.setContentAreaFilled(true);
		botao.setBorderPainted(true);
		botao.setFocusPainted(false);
		botao.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
		botao.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				botao.setBackground(fundoHover);
				botao.setForeground(frenteHover);
			}

			@Override
			public void mouseExited(MouseEvent e) {
				botao.setBackground(fundo);
				botao.setForeground(frente);
			}
		});
		return botao;
	}

	// ---------------- TEXTOS ----------------

	public static JLabel rotulo(String texto, Font fonte, Color cor) {
		JLabel rotulo = new JLabel(texto);
		rotulo.setFont(fonte);
		rotulo.setForeground(cor);
		return rotulo;
	}

	// ---------------- TABELAS ----------------

	/** Cabeçalho castanho, texto centrado e linhas alternadas. */
	public static void configurarTabela(JTable tabela) {
		tabela.setFont(FONTE_NORMAL);
		tabela.setRowHeight(30);
		tabela.setBackground(BRANCO);
		tabela.setForeground(TEXTO);
		tabela.setSelectionBackground(DOURADO);
		tabela.setSelectionForeground(TEXTO);
		tabela.setShowGrid(false);
		tabela.setIntercellSpacing(new Dimension(0, 0));
		tabela.setFillsViewportHeight(true);
		tabela.getTableHeader().setReorderingAllowed(false);

		JTableHeader cabecalho = tabela.getTableHeader();
		DefaultTableCellRenderer rendererCabecalho = new DefaultTableCellRenderer();
		rendererCabecalho.setHorizontalAlignment(SwingConstants.CENTER);
		rendererCabecalho.setBackground(CROSTA);
		rendererCabecalho.setForeground(BRANCO);
		rendererCabecalho.setFont(FONTE_NEGRITO);
		rendererCabecalho.setBorder(BorderFactory.createEmptyBorder(6, 6, 6, 6));
		cabecalho.setDefaultRenderer(rendererCabecalho);
		cabecalho.setPreferredSize(new Dimension(0, 34));

		tabela.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
			@Override
			public Component getTableCellRendererComponent(JTable t, Object valor, boolean seleccionada,
					boolean foco, int linha, int coluna) {
				super.getTableCellRendererComponent(t, valor, seleccionada, false, linha, coluna);
				setHorizontalAlignment(SwingConstants.CENTER);
				if (!seleccionada) {
					setBackground(linha % 2 == 1 ? PAINEL : BRANCO);
				}
				return this;
			}
		});
	}

	// ---------------- JANELAS ----------------

	/** Centra a janela no ecrã (um pouco acima do meio, como na versão Python). */
	public static void centrarJanela(Window janela) {
		Dimension ecra = Toolkit.getDefaultToolkit().getScreenSize();
		int x = (ecra.width - janela.getWidth()) / 2;
		int y = (ecra.height - janela.getHeight()) / 3;
		janela.setLocation(Math.max(x, 0), Math.max(y, 0));
	}

	/** Margem interior vazia, em píxeis. */
	public static void margem(JComponent componente, int vertical, int horizontal) {
		componente.setBorder(BorderFactory.createEmptyBorder(vertical, horizontal, vertical, horizontal));
	}


	private SistemaPadaria() {
	}
}
