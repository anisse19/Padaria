package listas_duplamente_ligadas;

/**
 * Um produto da padaria. É o "elemento" guardado em cada No da ListaProdutos.
 *
 * Para acrescentar um atributo: pô-lo aqui e no enum Atributo (no fim deste ficheiro).
 */
public class Produto {

	private int codigo;          // único na lista
	private String nome;
	private String categoria;
	private double preco;
	private int quantidade;      // stock disponível
	private String validade;     // "dd/mm/aaaa"

	public Produto(int codigo, String nome, String categoria, double preco, int quantidade, String validade) {
		this.codigo = codigo;
		this.nome = nome;
		this.categoria = categoria;
		this.preco = preco;
		this.quantidade = quantidade;
		this.validade = validade;
	}

	public int getCodigo() {
		return codigo;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getCategoria() {
		return categoria;
	}

	public void setCategoria(String categoria) {
		this.categoria = categoria;
	}

	public double getPreco() {
		return preco;
	}

	public void setPreco(double preco) {
		this.preco = preco;
	}

	public int getQuantidade() {
		return quantidade;
	}

	public void setQuantidade(int quantidade) {
		this.quantidade = quantidade;
	}

	public String getValidade() {
		return validade;
	}

	public void setValidade(String validade) {
		this.validade = validade;
	}

	/**
	 * Dois produtos são iguais se tiverem o mesmo código. É isto que permite
	 * usar ListaLigadas.contem(produto) para detectar códigos repetidos.
	 */
	@Override
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (!(obj instanceof Produto)) {
			return false;
		}
		return codigo == ((Produto) obj).codigo;
	}

	@Override
	public int hashCode() {
		return Integer.hashCode(codigo);
	}

	@Override
	public String toString() {
		return codigo + " - " + nome;
	}

	// ---------------- ATRIBUTOS ----------------

	/**
	 * Atributos do produto, pela ordem em que aparecem na tabela, na janela de
	 * produto e nas buscas. Substitui o getattr(produto, "nome") da versão Python.
	 */
	public enum Atributo {

		CODIGO("Código", null),
		NOME("Nome", null),
		CATEGORIA("Categoria", null),
		PRECO("Preço", SistemaPadaria.MOEDA),
		QUANTIDADE("Quantidade", null),
		VALIDADE("Validade", "dd/mm/aaaa");

		private final String rotulo;
		private final String dica;   // texto mostrado ao lado do campo na janela de produto

		Atributo(String rotulo, String dica) {
			this.rotulo = rotulo;
			this.dica = dica;
		}

		public String getRotulo() {
			return rotulo;
		}

		public String getDica() {
			return dica;
		}

		/** Valor deste atributo no produto (Integer, Double ou String). */
		public Comparable<?> valorEm(Produto produto) {
			switch (this) {
			case CODIGO:
				return produto.getCodigo();
			case NOME:
				return produto.getNome();
			case CATEGORIA:
				return produto.getCategoria();
			case PRECO:
				return produto.getPreco();
			case QUANTIDADE:
				return produto.getQuantidade();
			case VALIDADE:
				return produto.getValidade();
			default:
				throw new IllegalStateException("Atributo desconhecido: " + this);
			}
		}

		/** Usado pelas JComboBox para mostrar "Preço" em vez de "PRECO". */
		@Override
		public String toString() {
			return rotulo;
		}
	}
}
