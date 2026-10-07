package padaria.modelo;

/**
 * Um produto da padaria. É o "elemento" guardado em cada No da ListaProdutos.
 *
 * Para acrescentar um atributo: pô-lo aqui e no enum Atributo.
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
}
