package listas_duplamente_ligadas;


public class No {
	
	private No proximo;  
	private Object elemento;
	private No anterior;
		
	public No(Object elemento) {
		this.elemento = elemento;
		this.anterior = null;
		this.proximo = null;
	}

	public No(Object elemento, No proximo) {
		this.elemento = elemento;
		this.anterior = null;
		this.proximo = proximo;
	}

	public No(No anterior, Object elemento, No proximo) {
		this.anterior = anterior;
		this.elemento = elemento;
		this.proximo = proximo;
	}
		
	public void setProximo(No proximo) {  
		this.proximo = proximo;  
	}  
		
	public No getProximo() {  
		return proximo; 
	}  
		
	public Object getElemento() {  
		return elemento;  
	}

	public No getAnterior() {
		return anterior;
	}

	public void setAnterior(No anterior) {
		this.anterior = anterior;
	}  
		
}

