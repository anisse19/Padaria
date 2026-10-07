package listas_duplamente_ligadas;


/**
 * Lista duplamente ligada que guarda as vendas realizadas.
 *
 * Só se acrescenta (adicionaFim): as vendas não se alteram nem se apagam
 * (histórico de caixa).
 */
public class ListaVendas extends ListaLigadas {

	/** Não valida stock: essa regra está em AplicacaoPadaria.registarVenda. */
	public Venda registarVenda(int codigoProduto, String nomeProduto, int quantidade, double precoUnitario) {
		Venda venda = new Venda(codigoProduto, nomeProduto, quantidade, precoUnitario);
		adicionaFim(venda);
		return venda;
	}

	public double totalVendas() {
		double total = 0;
		for (int i = 0; i < tamanho(); i++) {
			total += ((Venda) pega(i)).getTotal();
		}
		return total;
	}

	public int totalQuantidade() {
		int total = 0;
		for (int i = 0; i < tamanho(); i++) {
			total += ((Venda) pega(i)).getQuantidade();
		}
		return total;
	}
}
