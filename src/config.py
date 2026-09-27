"""Configuração do sistema: utilizadores autorizados e permissões."""

# Em produção, as senhas nunca devem ficar em texto simples no código-fonte;
# aqui ficam assim apenas para efeitos do trabalho académico.

UTILIZADORES = {
    "dono": {
        "senha": "dono123",
        "tipo": "Dono da Padaria",
        "nome": "Proprietário(a)",
    },
    "funcionario": {
        "senha": "func123",
        "tipo": "Funcionário",
        "nome": "Funcionário(a)",
    },
}

# Operações que exigem perfil de Dono da Padaria.
OPERACOES_RESTRITAS_AO_DONO = {
    "Cadastrar",
    "Alterar (por código)",
    "Eliminar por posição",
    "Eliminar por código",
}
