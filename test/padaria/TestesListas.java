package padaria;

import java.util.Arrays;

import listas_duplamente_ligadas.IntefaceGeral;
import padaria.estruturas.ListaProdutos;
import padaria.estruturas.ListaVendas;
import padaria.modelo.Atributo;
import padaria.modelo.Produto;

/**
 * Testes das listas, sem bibliotecas externas. Correr com:
 *   java -cp bin padaria.TestesListas
 * Termina com código 1 se algum teste falhar.
 */
public class TestesListas {

	private static int falhas = 0;
	private static int executados = 0;

	public static void main(String[] args) {
		testar("cadastrar adiciona no fim", TestesListas::cadastrarAdicionaNoFim);
		testar("cadastrar código repetido falha", TestesListas::cadastrarCodigoRepetidoFalha);
		testar("buscar por código", TestesListas::buscarPorCodigo);
		testar("buscar por 1 atributo ignora maiúsculas", TestesListas::buscarPorUmAtributo);
		testar("buscar por 2 atributos", TestesListas::buscarPorDoisAtributos);
		testar("alterar ignora campos vazios", TestesListas::alterarIgnoraCamposVazios);
		testar("eliminar por posição", TestesListas::eliminarPorPosicao);
		testar("eliminar última posição", TestesListas::eliminarUltimaPosicao);
		testar("eliminar até esvaziar", TestesListas::eliminarAteEsvaziar);
		testar("eliminar por posição inválida", TestesListas::eliminarPorPosicaoInvalida);
		testar("eliminar por código", TestesListas::eliminarPorCodigo);
		testar("listar ordenado", TestesListas::listarOrdenado);
		testar("vendas: registar e totais", TestesListas::vendasRegistarETotais);

		System.out.println();
		System.out.println(executados + " testes, " + falhas + " falhas");
		if (falhas > 0) {
			System.exit(1);
		}
	}

	// ---------------- PRODUTOS ----------------

	private static ListaProdutos novaLista() {
		ListaProdutos lista = new ListaProdutos();
		lista.cadastrar(new Produto(1, "Pão de forma", "Pão", 80.0, 50, "15/09/2026"));
		lista.cadastrar(new Produto(2, "Bolo de chocolate", "Bolo", 350.0, 10, "12/09/2026"));
		lista.cadastrar(new Produto(3, "Pão careca", "Pão", 15.0, 100, "14/09/2026"));
		return lista;
	}

	private static void cadastrarAdicionaNoFim() {
		ListaProdutos lista = novaLista();
		igual(codigos(lista), new int[] { 1, 2, 3 });
		igual(lista.tamanho(), 3);
	}

	private static void cadastrarCodigoRepetidoFalha() {
		ListaProdutos lista = novaLista();
		try {
			lista.cadastrar(new Produto(1, "Outro", "Pão", 1.0, 1, ""));
			falhar("devia ter lançado IllegalArgumentException");
		} catch (IllegalArgumentException esperado) {
			igual(lista.tamanho(), 3);
		}
	}

	private static void buscarPorCodigo() {
		ListaProdutos lista = novaLista();
		igual(lista.buscarPorCodigo(2).getNome(), "Bolo de chocolate");
		verdade(lista.buscarPorCodigo(99) == null, "código 99 não devia existir");
	}

	private static void buscarPorUmAtributo() {
		igual(codigos(novaLista().buscarPorUmAtributo(Atributo.CATEGORIA, "pão")), new int[] { 1, 3 });
	}

	private static void buscarPorDoisAtributos() {
		IntefaceGeral resultado = novaLista().buscarPorDoisAtributos(
				Atributo.CATEGORIA, "Pão", Atributo.PRECO, "15.0");
		igual(codigos(resultado), new int[] { 3 });
	}

	private static void alterarIgnoraCamposVazios() {
		ListaProdutos lista = novaLista();
		lista.alterarPorCodigo(1, "", null, 90.0, null, null);
		Produto produto = lista.buscarPorCodigo(1);
		igual(produto.getNome(), "Pão de forma");
		igual(produto.getPreco(), 90.0);
		igual(produto.getQuantidade(), 50);
	}

	private static void eliminarPorPosicao() {
		ListaProdutos lista = novaLista();
		igual(lista.eliminarPorPosicao(2).getCodigo(), 2);
		igual(codigos(lista), new int[] { 1, 3 });
		igual(lista.eliminarPorPosicao(1).getCodigo(), 1);
		igual(codigos(lista), new int[] { 3 });
	}

	private static void eliminarUltimaPosicao() {
		ListaProdutos lista = novaLista();
		igual(lista.eliminarPorPosicao(3).getCodigo(), 3);
		igual(codigos(lista), new int[] { 1, 2 });
		// Depois de remover o último, adicionar no fim tem de continuar a funcionar.
		lista.cadastrar(new Produto(4, "Pastel de nata", "Doce", 45.0, 30, "13/09/2026"));
		igual(codigos(lista), new int[] { 1, 2, 4 });
	}

	private static void eliminarAteEsvaziar() {
		ListaProdutos lista = novaLista();
		for (int i = 0; i < 3; i++) {
			lista.eliminarPorPosicao(1);
		}
		verdade(lista.estaVazio(), "a lista devia estar vazia");
		igual(codigos(lista), new int[] {});
		// Uma lista esvaziada tem de voltar a aceitar produtos.
		lista.cadastrar(new Produto(5, "Broa", "Pão", 20.0, 5, "20/09/2026"));
		igual(codigos(lista), new int[] { 5 });
	}

	private static void eliminarPorPosicaoInvalida() {
		ListaProdutos lista = novaLista();
		try {
			lista.eliminarPorPosicao(4);
			falhar("devia ter lançado IndexOutOfBoundsException");
		} catch (IndexOutOfBoundsException esperado) {
			igual(lista.tamanho(), 3);
		}
	}

	private static void eliminarPorCodigo() {
		ListaProdutos lista = novaLista();
		lista.eliminarPorCodigo(3);
		igual(codigos(lista), new int[] { 1, 2 });
		lista.eliminarPorCodigo(1);
		igual(codigos(lista), new int[] { 2 });
		try {
			lista.eliminarPorCodigo(3);
			falhar("devia ter lançado IllegalArgumentException");
		} catch (IllegalArgumentException esperado) {
			igual(lista.tamanho(), 1);
		}
	}

	private static void listarOrdenado() {
		ListaProdutos lista = novaLista();
		igual(codigos(lista.listarOrdenado(Atributo.PRECO, false)), new int[] { 3, 1, 2 });
		igual(codigos(lista.listarOrdenado(Atributo.PRECO, true)), new int[] { 2, 1, 3 });
		igual(codigos(lista), new int[] { 1, 2, 3 });  // a lista original não muda
	}

	// ---------------- VENDAS ----------------

	private static void vendasRegistarETotais() {
		ListaVendas vendas = new ListaVendas();
		vendas.registarVenda(1, "Pão de forma", 10, 80.0);
		vendas.registarVenda(3, "Pastel de nata", 5, 45.0);

		igual(vendas.tamanho(), 2);
		igual(vendas.totalQuantidade(), 15);
		igual(vendas.totalVendas(), 1025.0);
	}

	// ---------------- MINI-FRAMEWORK ----------------

	private static int[] codigos(IntefaceGeral produtos) {
		int[] codigos = new int[produtos.tamanho()];
		for (int i = 0; i < codigos.length; i++) {
			codigos[i] = ((Produto) produtos.pega(i)).getCodigo();
		}
		return codigos;
	}

	private static void testar(String nome, Runnable teste) {
		executados++;
		try {
			teste.run();
			System.out.println("ok     " + nome);
		} catch (Throwable t) {
			falhas++;
			System.out.println("FALHOU " + nome + ": " + t);
		}
	}

	private static void falhar(String mensagem) {
		throw new AssertionError(mensagem);
	}

	private static void verdade(boolean condicao, String mensagem) {
		if (!condicao) {
			falhar(mensagem);
		}
	}

	private static void igual(Object obtido, Object esperado) {
		if (!obtido.equals(esperado)) {
			falhar("esperado <" + esperado + "> mas foi <" + obtido + ">");
		}
	}

	private static void igual(int[] obtido, int[] esperado) {
		if (!Arrays.equals(obtido, esperado)) {
			falhar("esperado " + Arrays.toString(esperado) + " mas foi " + Arrays.toString(obtido));
		}
	}
}
