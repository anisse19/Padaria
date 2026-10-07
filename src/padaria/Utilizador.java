package padaria;

/** Um utilizador do sistema. É o "perfil" que a AplicacaoPadaria recebe depois do login. */
public class Utilizador {

	private final String senha;
	private final String tipo;   // Config.PERFIL_DONO ou Config.PERFIL_FUNCIONARIO
	private final String nome;

	public Utilizador(String senha, String tipo, String nome) {
		this.senha = senha;
		this.tipo = tipo;
		this.nome = nome;
	}

	public boolean senhaCorrecta(String senhaIntroduzida) {
		return senha.equals(senhaIntroduzida);
	}

	public String getTipo() {
		return tipo;
	}

	public String getNome() {
		return nome;
	}

	public boolean eDono() {
		return Config.PERFIL_DONO.equals(tipo);
	}
}
