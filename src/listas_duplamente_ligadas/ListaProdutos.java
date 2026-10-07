package listas_duplamente_ligadas;

import listas_duplamente_ligadas.Produto.Atributo;


/**
 * Lista duplamente ligada que guarda os produtos da padaria.
 *
 * Herda de ListaLigadas: as ligações entre nós são todas tratadas lá
 * (adicionaFim, pega, removePosicao, ...). Aqui só está a lógica dos produtos,
 * que invoca esses métodos.
 *
 * As posições em ListaLigadas começam em 0; as que o utilizador vê começam em 1.
 */
public class ListaProdutos extends ListaLigadas {

	// ---------------- CADASTRO ----------------

	/** Insere no fim. O código tem de ser único (é a chave de tudo o resto). */
	public void cadastrar(Produto produto) {
		// contem() usa Produto.equals, que compara só o código.
		if (contem(produto)) {
			throw new IllegalArgumentException("Já existe um produto com o código " + produto.getCodigo() + ".");
		}
		adicionaFim(produto);
	}

	// ---------------- BUSCA ----------------

	public Produto buscarPorCodigo(int codigo) {
		int posicao = posicaoDoCodigo(codigo);
		if (posicao == -1) {
			return null;
		}
		return (Produto) pega(posicao);
	}

	/**
	 * Compara como texto, sem distinguir maiúsculas. Por isso o preço 15 só é
	 * encontrado escrevendo "15.0".
	 */
	public ListaLigadas buscarPorUmAtributo(Atributo atributo, String valor) {
		ListaLigadas resultados = new ListaLigadas();
		for (int i = 0; i < tamanho(); i++) {
			Produto produto = (Produto) pega(i);
			if (coincide(produto, atributo, valor)) {
				resultados.adicionaFim(produto);
			}
		}
		return resultados;
	}

	/** As duas condições têm de se verificar (E lógico). */
	public ListaLigadas buscarPorDoisAtributos(Atributo atributo1, String valor1, Atributo atributo2, String valor2) {
		ListaLigadas resultados = new ListaLigadas();
		for (int i = 0; i < tamanho(); i++) {
			Produto produto = (Produto) pega(i);
			if (coincide(produto, atributo1, valor1) && coincide(produto, atributo2, valor2)) {
				resultados.adicionaFim(produto);
			}
		}
		return resultados;
	}

	// ---------------- ALTERAÇÃO ----------------

	/** Valores null ou "" são ignorados (o campo mantém o valor actual). */
	public Produto alterarPorCodigo(int codigo, String nome, String categoria, Double preco, Integer quantidade,
			String validade) {
		Produto produto = buscarPorCodigo(codigo);
		if (produto == null) {
			throw new IllegalArgumentException("Produto com código " + codigo + " não encontrado.");
		}
		if (nome != null && !nome.isEmpty()) {
			produto.setNome(nome);
		}
		if (categoria != null && !categoria.isEmpty()) {
			produto.setCategoria(categoria);
		}
		if (preco != null) {
			produto.setPreco(preco);
		}
		if (quantidade != null) {
			produto.setQuantidade(quantidade);
		}
		if (validade != null && !validade.isEmpty()) {
			produto.setValidade(validade);
		}
		return produto;
	}

	// ---------------- ELIMINAÇÃO ----------------

	/** Posição começa em 1. Devolve o produto eliminado. */
	public Produto eliminarPorPosicao(int posicao) {
		if (!posicaoValida(posicao - 1)) {
			throw new IndexOutOfBoundsException("Posição inválida.");
		}
		Produto removido = (Produto) pega(posicao - 1);
		removePosicao(posicao - 1);
		return removido;
	}

	public Produto eliminarPorCodigo(int codigo) {
		if (estaVazio()) {
			throw new IllegalStateException("A lista está vazia.");
		}
		int posicao = posicaoDoCodigo(codigo);
		if (posicao == -1) {
			throw new IllegalArgumentException("Produto com código " + codigo + " não encontrado.");
		}
		Produto removido = (Produto) pega(posicao);
		removePosicao(posicao);
		return removido;
	}

	// ---------------- IMPRESSÃO ----------------
	// "Listar todos" é a própria lista: quem a mostra percorre-a com tamanho()/pega().

	public ListaLigadas listarPorCriterio(Atributo atributo, String valor) {
		return buscarPorUmAtributo(atributo, valor);
	}

	/**
	 * Bubble sort sobre uma cópia; a lista original não muda.
	 *
	 * Limite: a validade é texto, por isso "01/12/2026" fica antes de "15/09/2026".
	 */
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public ListaLigadas listarOrdenado(Atributo atributo, boolean decrescente) {
		Produto[] produtos = new Produto[tamanho()];
		for (int i = 0; i < produtos.length; i++) {
			produtos[i] = (Produto) pega(i);
		}

		int n = produtos.length;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n - i - 1; j++) {
				Comparable v1 = atributo.valorEm(produtos[j]);
				Comparable v2 = atributo.valorEm(produtos[j + 1]);
				int comparacao = v1.compareTo(v2);
				if ((comparacao > 0 && !decrescente) || (comparacao < 0 && decrescente)) {
					Produto temp = produtos[j];
					produtos[j] = produtos[j + 1];
					produtos[j + 1] = temp;
				}
			}
		}

		ListaLigadas ordenada = new ListaLigadas();
		for (Produto produto : produtos) {
			ordenada.adicionaFim(produto);
		}
		return ordenada;
	}

	// ---------------- AUXILIARES ----------------

	/** Posição (a partir de 0) do produto com este código, ou -1. */
	private int posicaoDoCodigo(int codigo) {
		for (int i = 0; i < tamanho(); i++) {
			if (((Produto) pega(i)).getCodigo() == codigo) {
				return i;
			}
		}
		return -1;
	}

	private static boolean coincide(Produto produto, Atributo atributo, String valor) {
		String valorAtributo = String.valueOf(atributo.valorEm(produto)).trim().toLowerCase();
		return valorAtributo.equals(valor.trim().toLowerCase());
	}
}
