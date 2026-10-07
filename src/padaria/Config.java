package padaria;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/** Configuração do sistema: valores de negócio que podem mudar sem mexer no resto do código. */
public final class Config {

	public static final String NOME_PADARIA = "Padaria Adonai";
	public static final String MOEDA = "MT";

	// Comparar sempre com estas constantes, nunca com texto escrito à mão.
	public static final String PERFIL_DONO = "Dono da Padaria";
	public static final String PERFIL_FUNCIONARIO = "Funcionário";

	// Senhas em texto simples: aceitável só num trabalho académico.
	public static final Map<String, Utilizador> UTILIZADORES = new HashMap<String, Utilizador>();
	static {
		UTILIZADORES.put("dono", new Utilizador("dono123", PERFIL_DONO, "Proprietário(a)"));
		UTILIZADORES.put("funcionario", new Utilizador("func123", PERFIL_FUNCIONARIO, "Funcionário(a)"));
	}

	// Operações reservadas ao Dono. Têm de ser iguais ao texto dos botões em
	// AplicacaoPadaria.construirSidebar.
	public static final Set<String> OPERACOES_RESTRITAS_AO_DONO = new HashSet<String>(Arrays.asList(
			"Cadastrar",
			"Alterar (por código)",
			"Eliminar por posição",
			"Eliminar por código"));

	private Config() {
	}
}
