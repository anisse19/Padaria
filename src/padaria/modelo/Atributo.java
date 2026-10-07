package padaria.modelo;

import padaria.Config;

/**
 * Atributos do produto, pela ordem em que aparecem na tabela, na janela de
 * produto e nas buscas. Substitui o getattr(produto, "nome") da versão Python.
 */
public enum Atributo {

	CODIGO("Código", null),
	NOME("Nome", null),
	CATEGORIA("Categoria", null),
	PRECO("Preço", Config.MOEDA),
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
