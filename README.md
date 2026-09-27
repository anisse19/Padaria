# Padaria

Sistema de Gestão de Padaria — Trabalho Prático 1 de Algoritmos e Estruturas de Dados
(ISUTC — Engenharia Informática e de Telecomunicações).

- **Estrutura de dados:** Lista Duplamente Ligada (produtos e vendas)
- **Interface gráfica:** Tkinter
- **Dependências:** nenhuma além da biblioteca padrão do Python 3

## Como executar

```bash
python main.py
```

Utilizadores de teste:

| Utilizador    | Senha     | Perfil          |
|---------------|-----------|-----------------|
| `dono`        | `dono123` | Dono da Padaria |
| `funcionario` | `func123` | Funcionário     |

O Funcionário não vê as operações de cadastrar, alterar e eliminar.

## Testes

```bash
python -m unittest discover -v
```

## Estrutura do projecto

```
Padaria/
├── main.py                     # Ponto de entrada
├── assets/
│   └── imagens/fundo.png       # Imagem da tela inicial
├── src/
│   ├── app.py                  # Liga os ecrãs: Tela inicial -> Login -> Aplicação
│   ├── config.py               # Utilizadores e operações restritas ao Dono
│   ├── estruturas/
│   │   ├── lista_produtos.py   # No + ListaLigada (produtos)
│   │   └── lista_vendas.py     # NoVenda + ListaVendas
│   └── interface/
│       ├── tela_inicial.py     # Splash com imagem e botão "Acessar"
│       ├── tela_login.py       # Autenticação
│       └── aplicacao.py        # Janela principal (sidebar, formulário, abas)
└── tests/
    ├── test_lista_produtos.py
    └── test_lista_vendas.py
```

## Operações

- Login com controlo de acesso (Dono da Padaria / Funcionário)
- Cadastro de produtos
- Busca por um atributo / por dois atributos combinados
- Alteração de dados (por código)
- Eliminação por posição / por código
- Impressão: todos / por critério / ordenados (bubble sort)
- Registo de vendas
