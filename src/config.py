"""Configuração do sistema: utilizadores autorizados e permissões."""



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
