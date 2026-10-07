package listas_duplamente_ligadas;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dialog;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.time.LocalTime;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;

import listas_duplamente_ligadas.Produto.Atributo;


/**
 * Janela principal do sistema (depois do login).
 *
 * <pre>
 *  ┌──────────────────────── barra de topo ────────────────────────┐
 *  │ marca · saudação · perfil                              [Sair] │
 *  ├──────────┬────────────────────────────────────────────────────┤
 *  │ sidebar  │ abas: [Registos] [Vendas]                          │
 *  │ (acções) │ tabela + resumo                                    │
 *  └──────────┴────────────────────────────────────────────────────┘
 * </pre>
 *
 * Esta classe só trata da interface: as operações sobre dados estão em
 * ListaProdutos / ListaVendas (que herdam de ListaLigadas).
 *
 * Para acrescentar uma operação:
 *  1. criar o método acao...() (diálogos com novaJanela/mostrarJanela);
 *  2. acrescentá-la à lista em construirSidebar;
 *  3. se for só do Dono: pô-la em SistemaPadaria.OPERACOES_RESTRITAS_AO_DONO e chamar
 *     exigeDono() no início.
 */
public class AplicacaoPadaria {

	private static final int LARGURA = 1150, ALTURA = 700;
	private static final int LARGURA_MIN = 950, ALTURA_MIN = 600;

	/** Recebe {atributo: texto} e devolve true para fechar a janela, ou false para a manter (ex.: erro). */
	private interface AoGravar {
		boolean gravar(Map<Atributo, String> dados, JDialog janela);
	}

	/** Atributo + valor escolhidos numa janela de busca. */
	private static class Criterio {
		Atributo atributo;
		String valor;
	}

	// Os dados vivem aqui e perdem-se ao sair.
	private final ListaProdutos lista = new ListaProdutos();
	private final ListaVendas listaVendas = new ListaVendas();

	private final JFrame root;
	private final Utilizador perfil;
	private final boolean eDono;
	private final Runnable aoTerminarSessao;

	private JTabbedPane abas;
	private JPanel tabRegistos;
	private JPanel tabVendas;
	private JTable tabelaRegistos;
	private DefaultTableModel modeloRegistos;
	private DefaultTableModel modeloVendas;
	private JLabel labelTotalQtd;
	private JLabel labelTotalVendas;

	public AplicacaoPadaria(JFrame root, Utilizador perfil, Runnable aoTerminarSessao) {
		this.root = root;
		this.perfil = perfil;
		this.eDono = perfil.eDono();
		this.aoTerminarSessao = aoTerminarSessao;

		root.setTitle(SistemaPadaria.NOME_PADARIA + " - Sistema de Gestão");

		popularExemplo();
		construirLayout();

		root.setResizable(true);
		root.setMinimumSize(new Dimension(LARGURA_MIN, ALTURA_MIN));
		root.setSize(LARGURA, ALTURA);
		SistemaPadaria.centrarJanela(root);
		root.revalidate();
		root.repaint();
	}

	// ---------------- LAYOUT PRINCIPAL ----------------

	private void construirLayout() {
		JPanel conteudo = new JPanel(new BorderLayout());
		conteudo.add(construirBarraTopo(), BorderLayout.NORTH);
		conteudo.add(construirSidebar(), BorderLayout.WEST);

		JPanel area = new JPanel(new BorderLayout());
		area.setBorder(BorderFactory.createEmptyBorder(14, 16, 14, 16));
		area.add(construirAbas(), BorderLayout.CENTER);
		conteudo.add(area, BorderLayout.CENTER);

		root.setContentPane(conteudo);
		root.getRootPane().setDefaultButton(null);
	}

	// ---------------- BARRA DE TOPO ----------------

	private JPanel construirBarraTopo() {
		JPanel topo = new JPanel(new BorderLayout());
		topo.setBackground(SistemaPadaria.PAINEL);
		topo.setBorder(BorderFactory.createEmptyBorder(10, 16, 10, 16));

		topo.add(SistemaPadaria.rotulo(SistemaPadaria.NOME_PADARIA, SistemaPadaria.FONTE_SECCAO, SistemaPadaria.CROSTA), BorderLayout.WEST);

		JPanel direita = new JPanel(new FlowLayout(FlowLayout.RIGHT, 0, 0));
		direita.setOpaque(false);
		direita.add(SistemaPadaria.rotulo(saudacao(), SistemaPadaria.FONTE_NORMAL, SistemaPadaria.TEXTO));
		direita.add(Box.createHorizontalStrut(24));
		direita.add(SistemaPadaria.rotulo("Perfil: " + perfil.getTipo(), SistemaPadaria.FONTE_PEQUENA, SistemaPadaria.TEXTO_SUAVE));
		direita.add(Box.createHorizontalStrut(16));
		JButton btnSair = SistemaPadaria.botaoSecundario("Sair");
		btnSair.addActionListener(e -> terminarSessao());
		direita.add(btnSair);
		topo.add(direita, BorderLayout.EAST);

		return topo;
	}

	private String saudacao() {
		int hora = LocalTime.now().getHour();
		String inicio;
		if (hora < 12) {
			inicio = "Bom dia";
		} else if (hora < 19) {
			inicio = "Boa tarde";
		} else {
			inicio = "Boa noite";
		}
		return inicio + ", " + perfil.getNome() + "! O forno já está quente";
	}

	private void terminarSessao() {
		int resposta = JOptionPane.showConfirmDialog(root, "Deseja terminar a sessão actual?",
				"Terminar sessão", JOptionPane.YES_NO_OPTION);
		if (resposta == JOptionPane.YES_OPTION) {
			root.dispose();
			aoTerminarSessao.run();
		}
	}

	// ---------------- SIDEBAR ----------------

	private JPanel construirSidebar() {
		JPanel sidebar = new JPanel();
		sidebar.setLayout(new BoxLayout(sidebar, BoxLayout.Y_AXIS));
		sidebar.setBackground(SistemaPadaria.CROSTA);
		sidebar.setPreferredSize(new Dimension(230, 0));  // largura fixa
		sidebar.setBorder(BorderFactory.createEmptyBorder(18, 8, 8, 8));

		JLabel titulo = SistemaPadaria.rotulo("Operações", SistemaPadaria.FONTE_SECCAO, SistemaPadaria.BRANCO);
		titulo.setBorder(BorderFactory.createEmptyBorder(0, 8, 12, 0));
		titulo.setAlignmentX(Component.LEFT_ALIGNMENT);
		sidebar.add(titulo);

		// O texto do botão é comparado com OPERACOES_RESTRITAS_AO_DONO:
		// mudar um obriga a mudar o outro.
		Map<String, Runnable> operacoes = new LinkedHashMap<String, Runnable>();
		operacoes.put("Buscar Produto", this::acaoBuscarProduto);
		operacoes.put("Registar Venda", this::registarVenda);
		operacoes.put("Cadastrar", this::acaoCadastrar);
		operacoes.put("Buscar (1 atributo)", this::acaoBuscarUmAtributo);
		operacoes.put("Buscar (2 atributos)", this::acaoBuscarDoisAtributos);
		operacoes.put("Alterar (por código)", this::acaoAlterar);
		operacoes.put("Eliminar por posição", this::acaoEliminarPosicao);
		operacoes.put("Eliminar por código", this::acaoEliminarCodigo);
		operacoes.put("Listar todos", this::acaoListarTodos);
		operacoes.put("Listar por critério", this::acaoListarCriterio);
		operacoes.put("Listar ordenado", this::acaoListarOrdenado);

		for (Map.Entry<String, Runnable> operacao : operacoes.entrySet()) {
			boolean restrita = SistemaPadaria.OPERACOES_RESTRITAS_AO_DONO.contains(operacao.getKey());
			if (restrita && !eDono) {
				continue;  // a operação nem sequer é apresentada a quem não é o Dono
			}
			final Runnable comando = operacao.getValue();
			JButton btn = SistemaPadaria.botaoSidebar(operacao.getKey());
			btn.setAlignmentX(Component.LEFT_ALIGNMENT);
			btn.setMaximumSize(new Dimension(Integer.MAX_VALUE, btn.getPreferredSize().height));
			btn.addActionListener(e -> comando.run());
			sidebar.add(btn);
			sidebar.add(Box.createVerticalStrut(1));
		}
		return sidebar;
	}

	// ---------------- ABAS (REGISTOS / VENDAS) ----------------

	private JTabbedPane construirAbas() {
		abas = new JTabbedPane();

		// --- Aba Registos: uma coluna por atributo ---
		String[] colunas = new String[Atributo.values().length];
		for (Atributo atributo : Atributo.values()) {
			colunas[atributo.ordinal()] = atributo.getRotulo();
		}
		modeloRegistos = modeloSoLeitura(colunas);
		tabelaRegistos = new JTable(modeloRegistos);
		SistemaPadaria.configurarTabela(tabelaRegistos);

		tabRegistos = new JPanel(new BorderLayout());
		tabRegistos.add(new JScrollPane(tabelaRegistos), BorderLayout.CENTER);
		abas.addTab("Registos", tabRegistos);

		// --- Aba Vendas ---
		modeloVendas = modeloSoLeitura(new String[] {
				"Data", "Código", "Produto", "Qtd Solicitada", "Preço Unitário", "Total" });
		JTable tabelaVendas = new JTable(modeloVendas);
		SistemaPadaria.configurarTabela(tabelaVendas);

		JPanel resumo = new JPanel(new BorderLayout());
		resumo.setBorder(BorderFactory.createEmptyBorder(8, 10, 8, 10));
		JPanel totais = new JPanel(new FlowLayout(FlowLayout.LEFT, 0, 0));
		labelTotalQtd = SistemaPadaria.rotulo("Total Qtd: 0", SistemaPadaria.FONTE_NEGRITO, SistemaPadaria.CROSTA);
		labelTotalVendas = SistemaPadaria.rotulo("Total Vendas: 0.00 " + SistemaPadaria.MOEDA, SistemaPadaria.FONTE_NEGRITO, SistemaPadaria.CROSTA);
		totais.add(labelTotalQtd);
		totais.add(Box.createHorizontalStrut(24));
		totais.add(labelTotalVendas);
		resumo.add(totais, BorderLayout.WEST);
		JButton btnRegistar = SistemaPadaria.botao("+ Registar Venda");
		btnRegistar.addActionListener(e -> registarVenda());
		resumo.add(btnRegistar, BorderLayout.EAST);

		tabVendas = new JPanel(new BorderLayout());
		tabVendas.add(new JScrollPane(tabelaVendas), BorderLayout.CENTER);
		tabVendas.add(resumo, BorderLayout.SOUTH);
		abas.addTab("Vendas", tabVendas);

		actualizarTabelaRegistos();
		actualizarTabelaVendas();
		return abas;
	}

	private static DefaultTableModel modeloSoLeitura(String[] colunas) {
		return new DefaultTableModel(colunas, 0) {
			@Override
			public boolean isCellEditable(int linha, int coluna) {
				return false;
			}
		};
	}

	// ---------------- DADOS DE EXEMPLO ----------------

	private void popularExemplo() {
		lista.cadastrar(new Produto(1, "Pão de forma", "Pão", 80.0, 50, "15/09/2026"));
		lista.cadastrar(new Produto(2, "Bolo de chocolate", "Bolo", 350.0, 10, "12/09/2026"));
		lista.cadastrar(new Produto(3, "Pastel de nata", "Doce", 45.0, 30, "13/09/2026"));
		lista.cadastrar(new Produto(4, "Pão careca", "Pão", 15.0, 100, "14/09/2026"));

		listaVendas.registarVenda(1, "Pão de forma", 10, 80.0);
		listaVendas.registarVenda(3, "Pastel de nata", 5, 45.0);
		listaVendas.registarVenda(2, "Bolo de chocolate", 2, 350.0);
	}

	// ---------------- ACTUALIZAR TABELAS ----------------
	// Apaga tudo e volta a inserir: simples, e rápido para centenas de linhas.

	/** Mostra todos os produtos. */
	private void actualizarTabelaRegistos() {
		actualizarTabelaRegistos(lista);
	}

	/** Mostra os produtos de qualquer lista (a principal, ou o resultado de uma busca). */
	private void actualizarTabelaRegistos(IntefaceGeral produtos) {
		modeloRegistos.setRowCount(0);
		for (int i = 0; i < produtos.tamanho(); i++) {
			Produto produto = (Produto) produtos.pega(i);
			Object[] linha = new Object[Atributo.values().length];
			for (Atributo atributo : Atributo.values()) {
				linha[atributo.ordinal()] = atributo.valorEm(produto);
			}
			modeloRegistos.addRow(linha);
		}
	}

	private void actualizarTabelaVendas() {
		modeloVendas.setRowCount(0);
		for (int i = 0; i < listaVendas.tamanho(); i++) {
			Venda v = (Venda) listaVendas.pega(i);
			modeloVendas.addRow(new Object[] {
					v.getData(), v.getCodigoProduto(), v.getNomeProduto(), v.getQuantidade(),
					String.format("%.2f", v.getPrecoUnitario()), String.format("%.2f", v.getTotal()) });
		}
		labelTotalQtd.setText("Total Qtd: " + listaVendas.totalQuantidade());
		labelTotalVendas.setText(String.format("Total Vendas: %.2f %s", listaVendas.totalVendas(), SistemaPadaria.MOEDA));
	}

	// ---------------- PERMISSÕES ----------------

	/** Segunda linha de defesa (a sidebar já esconde os botões). Devolve true se a acção deve parar. */
	private boolean exigeDono() {
		if (!eDono) {
			aviso(root, "Acesso restrito", "Esta operação está reservada ao Dono da Padaria.");
			return true;
		}
		return false;
	}

	// ---------------- ACÇÕES ----------------
	// As estruturas sinalizam erros com excepções (IllegalArgumentException,
	// IndexOutOfBoundsException, ...); as acções apanham-nas e mostram-nas.

	private void acaoBuscarProduto() {
		final JDialog janela = novaJanela("Buscar Produto");
		JPanel corpo = corpo(janela);

		final JTextField entradaCodigo = new JTextField(20);
		grelha(corpo, new JLabel("Código do Produto:"), 0, 0, 1);
		grelha(corpo, entradaCodigo, 0, 1, 1);

		Runnable buscar = () -> {
			Integer codigo = lerInteiro(entradaCodigo.getText());
			if (codigo == null) {
				aviso(janela, "Aviso", "Insira um código numérico válido.");
				return;
			}
			Produto produto = lista.buscarPorCodigo(codigo);
			if (produto == null) {
				info(janela, "Resultado", "Nenhum produto encontrado com código " + codigo + ".");
				return;
			}
			ListaLigadas resultado = new ListaLigadas();
			resultado.adicionaFim(produto);
			actualizarTabelaRegistos(resultado);
			abas.setSelectedComponent(tabRegistos);
			tabelaRegistos.setRowSelectionInterval(0, 0);
			janela.dispose();
		};
		entradaCodigo.addActionListener(e -> buscar.run());

		JButton btnBuscar = SistemaPadaria.botao("Buscar");
		btnBuscar.addActionListener(e -> buscar.run());
		grelha(corpo, btnBuscar, 1, 0, 2);
		mostrarJanela(janela);
	}

	private void acaoCadastrar() {
		if (exigeDono()) {
			return;
		}
		janelaProduto("Cadastrar Produto", "Cadastrar", (dados, janela) -> {
			Integer codigo = lerInteiro(dados.get(Atributo.CODIGO));
			Double preco = lerDecimal(dados.get(Atributo.PRECO));
			Integer quantidade = lerInteiro(dados.get(Atributo.QUANTIDADE));
			if (codigo == null || preco == null || quantidade == null) {
				erro(janela, "Verifique os campos numéricos (código, preço, quantidade).");
				return false;
			}
			try {
				lista.cadastrar(new Produto(codigo, dados.get(Atributo.NOME), dados.get(Atributo.CATEGORIA),
						preco, quantidade, dados.get(Atributo.VALIDADE)));
			} catch (IllegalArgumentException e) {  // ex.: código repetido
				erro(janela, e.getMessage());
				return false;
			}
			actualizarTabelaRegistos();
			abas.setSelectedComponent(tabRegistos);
			info(janela, "Sucesso", "Produto cadastrado com sucesso.");
			return true;
		}, null);
	}

	/** Pede o código e abre a janela de produto já preenchida. */
	private void acaoAlterar() {
		if (exigeDono()) {
			return;
		}
		String texto = pedirValorSimples("Alterar Produto", "Código do produto:");
		if (texto == null) {
			return;
		}
		final Integer codigo = lerInteiro(texto);
		if (codigo == null) {
			aviso(root, "Aviso", "Insira um código numérico válido.");
			return;
		}
		Produto produto = lista.buscarPorCodigo(codigo);
		if (produto == null) {
			erro(root, "Produto com código " + codigo + " não encontrado.");
			return;
		}

		janelaProduto("Alterar Produto " + codigo, "Guardar alterações", (dados, janela) -> {
			// Campos numéricos vazios passam como null e são ignorados.
			String textoPreco = dados.get(Atributo.PRECO);
			String textoQuantidade = dados.get(Atributo.QUANTIDADE);
			Double preco = textoPreco.isEmpty() ? null : lerDecimal(textoPreco);
			Integer quantidade = textoQuantidade.isEmpty() ? null : lerInteiro(textoQuantidade);
			if ((!textoPreco.isEmpty() && preco == null) || (!textoQuantidade.isEmpty() && quantidade == null)) {
				erro(janela, "Preço e quantidade têm de ser numéricos.");
				return false;
			}
			lista.alterarPorCodigo(codigo, dados.get(Atributo.NOME), dados.get(Atributo.CATEGORIA),
					preco, quantidade, dados.get(Atributo.VALIDADE));
			actualizarTabelaRegistos();
			info(janela, "Sucesso", "Produto alterado com sucesso.");
			return true;
		}, produto);
	}

	private void acaoBuscarUmAtributo() {
		Criterio criterio = pedirAtributoValor("Buscar por 1 atributo");
		if (criterio == null) {
			return;
		}
		ListaLigadas resultados = lista.buscarPorUmAtributo(criterio.atributo, criterio.valor);
		actualizarTabelaRegistos(resultados);
		abas.setSelectedComponent(tabRegistos);
		if (resultados.estaVazio()) {
			info(root, "Busca", "Nenhum produto encontrado.");
		}
	}

	private void acaoBuscarDoisAtributos() {
		final JDialog janela = novaJanela("Buscar por 2 atributos");
		JPanel corpo = corpo(janela);

		final JComboBox<Atributo> combo1 = comboAtributos();
		final JTextField entrada1 = new JTextField(15);
		grelha(corpo, new JLabel("Atributo 1:"), 0, 0, 1);
		grelha(corpo, combo1, 0, 1, 1);
		grelha(corpo, entrada1, 0, 2, 1);

		final JComboBox<Atributo> combo2 = comboAtributos();
		final JTextField entrada2 = new JTextField(15);
		grelha(corpo, new JLabel("Atributo 2:"), 1, 0, 1);
		grelha(corpo, combo2, 1, 1, 1);
		grelha(corpo, entrada2, 1, 2, 1);

		JButton btnBuscar = SistemaPadaria.botao("Buscar");
		btnBuscar.addActionListener(e -> {
			Atributo atributo1 = (Atributo) combo1.getSelectedItem();
			Atributo atributo2 = (Atributo) combo2.getSelectedItem();
			if (atributo1 == null || atributo2 == null) {
				aviso(janela, "Aviso", "Escolha os dois atributos.");
				return;
			}
			ListaLigadas resultados = lista.buscarPorDoisAtributos(
					atributo1, entrada1.getText(), atributo2, entrada2.getText());
			actualizarTabelaRegistos(resultados);
			abas.setSelectedComponent(tabRegistos);
			janela.dispose();
			if (resultados.estaVazio()) {
				info(root, "Busca", "Nenhum produto encontrado.");
			}
		});
		grelha(corpo, btnBuscar, 2, 0, 3);
		mostrarJanela(janela);
	}

	private void acaoEliminarPosicao() {
		if (exigeDono()) {
			return;
		}
		String texto = pedirValorSimples("Eliminar por posição", "Posição (1 = primeiro):");
		if (texto == null) {
			return;
		}
		Integer posicao = lerInteiro(texto);
		if (posicao == null) {
			erro(root, "Insira uma posição numérica válida.");
			return;
		}
		try {
			Produto removido = lista.eliminarPorPosicao(posicao);
			actualizarTabelaRegistos();
			info(root, "Sucesso", "Produto '" + removido.getNome() + "' eliminado.");
		} catch (IndexOutOfBoundsException e) {
			erro(root, e.getMessage());
		}
	}

	private void acaoEliminarCodigo() {
		if (exigeDono()) {
			return;
		}
		String texto = pedirValorSimples("Eliminar por código", "Código:");
		if (texto == null) {
			return;
		}
		Integer codigo = lerInteiro(texto);
		if (codigo == null) {
			erro(root, "Insira um código numérico válido.");
			return;
		}
		try {
			Produto removido = lista.eliminarPorCodigo(codigo);
			actualizarTabelaRegistos();
			info(root, "Sucesso", "Produto '" + removido.getNome() + "' eliminado.");
		} catch (IllegalArgumentException | IllegalStateException e) {
			erro(root, e.getMessage());
		}
	}

	private void acaoListarTodos() {
		actualizarTabelaRegistos();
		abas.setSelectedComponent(tabRegistos);
	}

	private void acaoListarCriterio() {
		Criterio criterio = pedirAtributoValor("Listar por critério");
		if (criterio == null) {
			return;
		}
		actualizarTabelaRegistos(lista.listarPorCriterio(criterio.atributo, criterio.valor));
		abas.setSelectedComponent(tabRegistos);
	}

	private void acaoListarOrdenado() {
		final JDialog janela = novaJanela("Listar ordenado");
		JPanel corpo = corpo(janela);

		final JComboBox<Atributo> combo = comboAtributos();
		grelha(corpo, new JLabel("Ordenar por:"), 0, 0, 1);
		grelha(corpo, combo, 0, 1, 1);

		final JCheckBox decrescente = new JCheckBox("Ordem decrescente");
		decrescente.setOpaque(false);
		grelha(corpo, decrescente, 1, 0, 2);

		JButton btnOrdenar = SistemaPadaria.botao("Ordenar");
		btnOrdenar.addActionListener(e -> {
			Atributo atributo = (Atributo) combo.getSelectedItem();
			if (atributo == null) {
				aviso(janela, "Aviso", "Escolha o atributo para ordenar.");
				return;
			}
			actualizarTabelaRegistos(lista.listarOrdenado(atributo, decrescente.isSelected()));
			abas.setSelectedComponent(tabRegistos);
			janela.dispose();
		});
		grelha(corpo, btnOrdenar, 2, 0, 2);
		mostrarJanela(janela);
	}

	// ---------------- REGISTAR VENDA ----------------

	/** As regras da venda (quantidade > 0, produto existe, stock chega) estão aqui. */
	private void registarVenda() {
		final JDialog janela = novaJanela("Registar Venda");
		JPanel corpo = corpo(janela);

		final JTextField entradaCodigo = new JTextField(20);
		final JTextField entradaQtd = new JTextField(20);
		grelha(corpo, new JLabel("Código do Produto:"), 0, 0, 1);
		grelha(corpo, entradaCodigo, 0, 1, 1);
		grelha(corpo, new JLabel("Quantidade:"), 1, 0, 1);
		grelha(corpo, entradaQtd, 1, 1, 1);

		Runnable confirmar = () -> {
			Integer codigo = lerInteiro(entradaCodigo.getText());
			Integer qtd = lerInteiro(entradaQtd.getText());
			if (codigo == null || qtd == null || qtd <= 0) {
				aviso(janela, "Aviso", "Código e quantidade devem ser numéricos positivos.");
				return;
			}

			Produto produto = lista.buscarPorCodigo(codigo);
			if (produto == null) {
				erro(janela, "Produto com código " + codigo + " não encontrado.");
				return;
			}
			if (qtd > produto.getQuantidade()) {
				aviso(janela, "Aviso", "Estoque insuficiente. Disponível: " + produto.getQuantidade());
				return;
			}

			// Só desconta o stock depois de todas as validações passarem.
			produto.setQuantidade(produto.getQuantidade() - qtd);
			listaVendas.registarVenda(codigo, produto.getNome(), qtd, produto.getPreco());
			actualizarTabelaRegistos();
			actualizarTabelaVendas();
			abas.setSelectedComponent(tabVendas);
			info(janela, "Sucesso", String.format("Venda registada: %dx %s = %.2f %s",
					qtd, produto.getNome(), qtd * produto.getPreco(), SistemaPadaria.MOEDA));
			janela.dispose();
		};
		entradaCodigo.addActionListener(e -> entradaQtd.requestFocusInWindow());
		entradaQtd.addActionListener(e -> confirmar.run());

		JButton btnRegistar = SistemaPadaria.botao("Registar Venda");
		btnRegistar.addActionListener(e -> confirmar.run());
		grelha(corpo, btnRegistar, 2, 0, 2);
		mostrarJanela(janela);
	}

	// ---------------- JANELAS AUXILIARES ----------------
	// Todos os diálogos: novaJanela -> componentes em corpo(janela) -> mostrarJanela.

	/** Janela modal com um corpo em grelha que já tem margens. */
	private JDialog novaJanela(String titulo) {
		JDialog janela = new JDialog(root, titulo, Dialog.ModalityType.APPLICATION_MODAL);
		janela.setResizable(false);
		JPanel corpo = new JPanel(new GridBagLayout());
		corpo.setBorder(BorderFactory.createEmptyBorder(24, 24, 24, 24));
		janela.setContentPane(corpo);
		return janela;
	}

	private static JPanel corpo(JDialog janela) {
		return (JPanel) janela.getContentPane();
	}

	/** Centra sobre a janela principal e mostra. Bloqueia até a janela fechar. */
	private void mostrarJanela(JDialog janela) {
		janela.pack();
		janela.setLocationRelativeTo(root);
		janela.setVisible(true);
	}

	/** Coloca um componente na grelha do corpo; os botões (largura > 1) ficam centrados por baixo. */
	private static void grelha(JPanel corpo, Component componente, int linha, int coluna, int largura) {
		GridBagConstraints c = new GridBagConstraints();
		c.gridy = linha;
		c.gridx = coluna;
		c.gridwidth = largura;
		c.insets = new Insets(largura > 1 ? 12 : 6, 5, 6, 5);
		c.anchor = coluna == 0 && largura == 1 ? GridBagConstraints.EAST : GridBagConstraints.CENTER;
		c.fill = componente instanceof JTextField || componente instanceof JComboBox
				? GridBagConstraints.HORIZONTAL : GridBagConstraints.NONE;
		corpo.add(componente, c);
	}

	/**
	 * Janela com um campo por atributo, usada por Cadastrar e Alterar.
	 * Com produto != null, os campos vêm preenchidos e o código fica bloqueado.
	 */
	private void janelaProduto(String titulo, String textoBotao, final AoGravar aoConfirmar, Produto produto) {
		final JDialog janela = novaJanela(titulo);
		JPanel corpo = corpo(janela);

		GridBagConstraints c = new GridBagConstraints();
		c.gridx = 0;
		c.gridy = 0;
		c.gridwidth = 3;
		c.anchor = GridBagConstraints.WEST;
		c.insets = new Insets(0, 0, 14, 0);
		corpo.add(SistemaPadaria.rotulo(titulo, SistemaPadaria.FONTE_SECCAO, SistemaPadaria.CROSTA), c);

		final Map<Atributo, JTextField> entradas = new EnumMap<Atributo, JTextField>(Atributo.class);
		for (Atributo atributo : Atributo.values()) {
			int linha = atributo.ordinal() + 1;
			grelha(corpo, new JLabel(atributo.getRotulo() + ":"), linha, 0, 1);
			JTextField entrada = new JTextField(22);
			if (produto != null) {
				entrada.setText(String.valueOf(atributo.valorEm(produto)));
			}
			grelha(corpo, entrada, linha, 1, 1);
			if (atributo.getDica() != null) {
				JLabel dica = SistemaPadaria.rotulo(atributo.getDica(), SistemaPadaria.FONTE_PEQUENA, SistemaPadaria.TEXTO_SUAVE);
				GridBagConstraints cd = new GridBagConstraints();
				cd.gridx = 2;
				cd.gridy = linha;
				cd.anchor = GridBagConstraints.WEST;
				cd.insets = new Insets(0, 8, 0, 0);
				corpo.add(dica, cd);
			}
			entradas.put(atributo, entrada);
		}
		if (produto != null) {
			entradas.get(Atributo.CODIGO).setEnabled(false);  // o código identifica o produto
		}

		JButton btnConfirmar = SistemaPadaria.botao(textoBotao);
		btnConfirmar.addActionListener(e -> {
			Map<Atributo, String> dados = new EnumMap<Atributo, String>(Atributo.class);
			for (Map.Entry<Atributo, JTextField> entrada : entradas.entrySet()) {
				dados.put(entrada.getKey(), entrada.getValue().getText().trim());
			}
			if (aoConfirmar.gravar(dados, janela)) {
				janela.dispose();
			}
		});
		GridBagConstraints cb = new GridBagConstraints();
		cb.gridx = 0;
		cb.gridy = Atributo.values().length + 1;
		cb.gridwidth = 3;
		cb.fill = GridBagConstraints.HORIZONTAL;
		cb.insets = new Insets(18, 0, 0, 0);
		corpo.add(btnConfirmar, cb);

		janela.getRootPane().setDefaultButton(btnConfirmar);  // Enter = confirmar
		mostrarJanela(janela);
	}

	/** Combobox com os atributos ("Preço", ...), sem nenhum escolhido. */
	private static JComboBox<Atributo> comboAtributos() {
		JComboBox<Atributo> combo = new JComboBox<Atributo>(Atributo.values());
		combo.setSelectedIndex(-1);
		return combo;
	}

	/** Bloqueia até a janela fechar. Devolve null se o utilizador fechar sem confirmar. */
	private Criterio pedirAtributoValor(String titulo) {
		final JDialog janela = novaJanela(titulo);
		JPanel corpo = corpo(janela);
		final Criterio[] resultado = { null };  // array: a lambda pode alterá-lo

		final JComboBox<Atributo> combo = comboAtributos();
		final JTextField entrada = new JTextField(18);
		grelha(corpo, new JLabel("Atributo:"), 0, 0, 1);
		grelha(corpo, combo, 0, 1, 1);
		grelha(corpo, new JLabel("Valor:"), 1, 0, 1);
		grelha(corpo, entrada, 1, 1, 1);

		Runnable confirmar = () -> {
			Atributo atributo = (Atributo) combo.getSelectedItem();
			if (atributo == null) {
				aviso(janela, "Aviso", "Escolha um atributo.");
				return;
			}
			Criterio criterio = new Criterio();
			criterio.atributo = atributo;
			criterio.valor = entrada.getText();
			resultado[0] = criterio;
			janela.dispose();
		};
		entrada.addActionListener(e -> confirmar.run());

		JButton btnConfirmar = SistemaPadaria.botao("Confirmar");
		btnConfirmar.addActionListener(e -> confirmar.run());
		grelha(corpo, btnConfirmar, 2, 0, 2);
		mostrarJanela(janela);

		return resultado[0];
	}

	/** Como pedirAtributoValor, só com um campo. Devolve o texto ou null. */
	private String pedirValorSimples(String titulo, String textoRotulo) {
		final JDialog janela = novaJanela(titulo);
		JPanel corpo = corpo(janela);
		final String[] resultado = { null };

		final JTextField entrada = new JTextField(18);
		grelha(corpo, new JLabel(textoRotulo), 0, 0, 1);
		grelha(corpo, entrada, 0, 1, 1);

		Runnable confirmar = () -> {
			resultado[0] = entrada.getText();
			janela.dispose();
		};
		entrada.addActionListener(e -> confirmar.run());

		JButton btnConfirmar = SistemaPadaria.botao("Confirmar");
		btnConfirmar.addActionListener(e -> confirmar.run());
		grelha(corpo, btnConfirmar, 1, 0, 2);
		mostrarJanela(janela);

		return resultado[0];
	}

	// ---------------- MENSAGENS E CONVERSÕES ----------------

	private static void info(Component pai, String titulo, String texto) {
		JOptionPane.showMessageDialog(pai, texto, titulo, JOptionPane.INFORMATION_MESSAGE);
	}

	private static void aviso(Component pai, String titulo, String texto) {
		JOptionPane.showMessageDialog(pai, texto, titulo, JOptionPane.WARNING_MESSAGE);
	}

	private static void erro(Component pai, String texto) {
		JOptionPane.showMessageDialog(pai, texto, "Erro", JOptionPane.ERROR_MESSAGE);
	}

	/** Inteiro escrito pelo utilizador, ou null se não for um número. */
	private static Integer lerInteiro(String texto) {
		try {
			return Integer.parseInt(texto.trim());
		} catch (NumberFormatException e) {
			return null;
		}
	}

	/** Aceita "12.5" e "12,5". Devolve null se não for um número. */
	private static Double lerDecimal(String texto) {
		try {
			return Double.parseDouble(texto.trim().replace(',', '.'));
		} catch (NumberFormatException e) {
			return null;
		}
	}
}
