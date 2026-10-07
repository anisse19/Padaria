package listas_duplamente_ligadas;

public class ListaLigadas implements IntefaceGeral{
	private No primeiro;
	
	private No ultimo;
	private int totalElem;
	
	public ListaLigadas() {
		primeiro = null;
		ultimo = null;
		totalElem = 0;
	}

	@Override
	public void adicionaInicio(Object elemento) {

	    No novo = new No(elemento);

	    novo.setAnterior(null);
	    novo.setProximo(primeiro);

	    if (estaVazio()) {
	        primeiro = novo;
	        ultimo = novo;
	    } else {
	        primeiro.setAnterior(novo);
	        primeiro = novo;
	    }

	    totalElem++;
	}
	@Override
	public void adicionaPosicao(int posicao, Object elemento) {
		// TODO Auto-generated method stub
		if (posicao < 0 || posicao > totalElem) {
			throw new IndexOutOfBoundsException("Posição inválida");
		}

		if (posicao == 0 || estaVazio()) {
			adicionaInicio(elemento);
			return;
		}

		if (posicao == totalElem) {
			adicionaFim(elemento);
			return;
		}
		
		No novo= new No(elemento);
		novo.setProximo(this.pegaNo(posicao));
		novo.setAnterior(pegaNo(posicao-1));
		novo.getAnterior().setProximo(novo);
		novo.getProximo().setAnterior(novo);
		totalElem++;
		
		
	}

	@Override
	public void adicionaFim(Object elemento) {
		// TODO Auto-generated method stub
		No novo = new No(elemento);
		if(estaVazio()) {
			adicionaInicio(elemento);
			return;
		}
		
		ultimo.setProximo(novo);
		novo.setAnterior(ultimo);
		ultimo=novo;
		totalElem++;
		
	}

	@Override
	public Object pega(int posicao) {
		// TODO Auto-generated method stub
		if(!posicaoValida(posicao)) {
			throw new IndexOutOfBoundsException("Posicao Invalida");
		}
		No actual = primeiro;

		for (int i = 0; i < posicao; i++) {
			actual = actual.getProximo();
		}

		return actual.getElemento();
		
	}
	

	@Override
	public void removeInicio() {
		// TODO Auto-generated method stub
		if (estaVazio()) {
			throw new IllegalStateException("A lista está vazia");
		}
		
		if(totalElem==1) {
			primeiro=null;
			ultimo=null;
			
			totalElem--;
			return;
		}

		primeiro = primeiro.getProximo();
		primeiro.setAnterior(null);

		totalElem--;

		if (totalElem == 0) {
			ultimo = null;
		}
		
	}

	@Override
	public void removePosicao(int posicao) {

	    if (!posicaoValida(posicao)) {
	        throw new IndexOutOfBoundsException("Posição inválida");
	    }

	    if (posicao == 0) {
	        removeInicio();
	        return;
	    }

	    if (posicao == totalElem - 1) {
	        removeFim();
	        return;
	    }

	    No actual = pegaNo(posicao);

	    actual.getAnterior().setProximo(actual.getProximo());
	    actual.getProximo().setAnterior(actual.getAnterior());

	    totalElem--;
	}

	@Override
	public void removeFim() {
		// TODO Auto-generated method stub
		if (estaVazio()) {
	        throw new NullPointerException("A lista está vazia");
	    }
		
		if(totalElem==1) {
			primeiro=null;
			ultimo=null;
			
			totalElem--;
			return;
		}
		
		ultimo=this.ultimo.getAnterior();
		ultimo.setProximo(null);
		totalElem--;
	}

	@Override
	public boolean contem(Object elemento) {
		// TODO Auto-generated method stub
		No actual = primeiro;

		while (actual != null) {

			if (actual.getElemento().equals(elemento)) {
				return true;
			}

			actual = actual.getProximo();
		}

		return false;
	}

	@Override
	public int tamanho() {
		// TODO Auto-generated method stub
		return totalElem;
	}

	@Override
	public boolean posicaoValida(int posicao) {
		// TODO Auto-generated method stub
		if (posicao < 0 || posicao >= totalElem) {
			return false;
		}
		
		return true;
	}

	@Override
	public boolean estaVazio() {
		// TODO Auto-generated method stub
		if(totalElem==0) {
			return true;
		}
		return false;
	}
	
	private No pegaNo(int posicao) {
		if (!posicaoValida(posicao)) {
			throw new IndexOutOfBoundsException("Posição inválida");
		}

		No actual = primeiro;
		
		for (int i = 0; i < posicao; i++) {
			actual = actual.getProximo();
		}

		return actual;
		
	}
	
	public void concatenar(ListaLigadas lista) {

		if (lista.estaVazio()) {
	    	throw new NullPointerException("A lista que deseja adicionar está vazia");
	    }

		if (this.estaVazio()) {
			this.primeiro = lista.primeiro;
			this.ultimo = lista.ultimo;
			this.totalElem = lista.totalElem;
			return;
		}

		this.ultimo.setProximo(lista.primeiro);
		lista.primeiro.setAnterior(this.ultimo);

		this.ultimo = lista.ultimo;
		this.totalElem += lista.totalElem;
	}
	
	public void RemoverTudo(Object obj) {

		No actual = primeiro;
		
		if(obj==null) {
			throw new NullPointerException("Não é possivel remover");
		}

		while (actual != null) {

			No proximo = actual.getProximo();

			if (actual.getElemento().equals(obj)) {

				if (actual == primeiro) {
					removeInicio();

				} else if (actual == ultimo) {
					removeFim();

				} else {
					actual.getAnterior().setProximo(actual.getProximo());
					actual.getProximo().setAnterior(actual.getAnterior());
					totalElem--;
				}
			}

			actual = proximo;
		}
	}
	
	public ListaLigadas contem(IntefaceGeral lista) {

		ListaLigadas encontrados = new ListaLigadas();

		for (int i = 0; i < lista.tamanho(); i++) {

			Object elemento = lista.pega(i);

			if (contem(elemento)) {
				encontrados.adicionaFim(elemento);
			}
		}

		return encontrados;
	}
	
	public int[] Ocorrencias(IntefaceGeral lista) {

		int[] ocorre = new int[lista.tamanho()];

		for (int i = 0; i < lista.tamanho(); i++) {

			Object elemento = lista.pega(i);

			No actual = primeiro;

			while (actual != null) {

				if (actual.getElemento().equals(elemento)) {
					ocorre[i]++;
				}

				actual = actual.getProximo();
			}
		}

		return ocorre;
	}

}
