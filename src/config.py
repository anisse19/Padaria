"""Configuração do sistema: valores de negócio que podem mudar sem mexer no código."""

NOME_PADARIA = "Padaria Adonai"
MOEDA = "MT"

# Comparar sempre com estas constantes, nunca com texto escrito à mão.
PERFIL_DONO = "Dono da Padaria"
PERFIL_FUNCIONARIO = "Funcionário"

# Senhas em texto simples: aceitável só num trabalho académico. Numa versão
# real, guardar um hash (hashlib) e ler de um ficheiro/base de dados.
UTILIZADORES = {
    "dono": {
        "senha": "dono123",
        "tipo": PERFIL_DONO,
        "nome": "Proprietário(a)",
    },
    "funcionario": {
        "senha": "func123",
        "tipo": PERFIL_FUNCIONARIO,
        "nome": "Funcionário(a)",
    },
}

# Identificadores das operações (ver AplicacaoPadaria._construir_sidebar)
# reservadas ao Dono. São os identificadores, não o texto dos botões.
OPERACOES_RESTRITAS_AO_DONO = {
    "Cadastrar",
    "Alterar (por código)",
    "Eliminar por posição",
    "Eliminar por código",
}
