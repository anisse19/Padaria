package listas_duplamente_ligadas;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Uma venda realizada. É o "elemento" guardado em cada No da ListaVendas.
 *
 * Guarda uma cópia do nome e do preço no momento da venda, para o histórico
 * não mudar se o produto for alterado ou eliminado depois.
 */
public class Venda {

	private static final DateTimeFormatter FORMATO_DATA = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

	private final int codigoProduto;
	private final String nomeProduto;
	private final int quantidade;
	private final double precoUnitario;
	private final double total;
	private final String data;

	public Venda(int codigoProduto, String nomeProduto, int quantidade, double precoUnitario) {
		this.codigoProduto = codigoProduto;
		this.nomeProduto = nomeProduto;
		this.quantidade = quantidade;
		this.precoUnitario = precoUnitario;
		this.total = quantidade * precoUnitario;
		this.data = LocalDateTime.now().format(FORMATO_DATA);
	}

	public int getCodigoProduto() {
		return codigoProduto;
	}

	public String getNomeProduto() {
		return nomeProduto;
	}

	public int getQuantidade() {
		return quantidade;
	}

	public double getPrecoUnitario() {
		return precoUnitario;
	}

	public double getTotal() {
		return total;
	}

	public String getData() {
		return data;
	}
}
