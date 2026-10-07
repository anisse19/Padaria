# Padaria

Sistema de Gestão de Padaria — Trabalho Prático 1 de Algoritmos e Estruturas de Dados
(ISUTC — Engenharia Informática e de Telecomunicações).

- **Linguagem:** Java (8 ou superior)
- **Estrutura de dados:** Lista Duplamente Ligada (`ListaLigadas`), usada para produtos e vendas
- **Interface gráfica:** Swing
- **Dependências:** nenhuma além da biblioteca padrão do Java

## Como executar

No Eclipse: *File → Import → Existing Projects into Workspace*, escolher esta pasta
e correr `padaria.Main`.

Na linha de comandos, a partir da raiz do projecto:

```bash
javac -encoding UTF-8 -d bin $(find src test -name "*.java")
java -cp bin padaria.Main
```

Utilizadores de teste:

| Utilizador    | Senha     | Perfil          |
|---------------|-----------|-----------------|
| `dono`        | `dono123` | Dono da Padaria |
| `funcionario` | `func123` | Funcionário     |

O Funcionário não vê as operações de cadastrar, alterar e eliminar.

## Testes

```bash
java -cp bin padaria.TestesListas
```

## Estrutura do projecto

```
Padaria/
├── assets/
│   └── imagens/fundo.png                 # Imagem da tela inicial
├── src/
│   ├── listas_duplamente_ligadas/        # Base: a lista duplamente ligada
│   │   ├── IntefaceGeral.java            #   operações da lista
│   │   ├── No.java                       #   nó (anterior, elemento, próximo)
│   │   └── ListaLigadas.java             #   implementação
│   └── padaria/
│       ├── Main.java                     # Ponto de entrada: Tela inicial -> Login -> Aplicação
│       ├── Config.java                   # Nome da padaria, moeda, utilizadores e permissões
│       ├── Utilizador.java
│       ├── modelo/
│       │   ├── Produto.java              # Elemento guardado na lista de produtos
│       │   ├── Venda.java                # Elemento guardado na lista de vendas
│       │   └── Atributo.java             # Atributos do produto (para buscas e ordenação)
│       ├── estruturas/
│       │   ├── ListaProdutos.java        # extends ListaLigadas
│       │   └── ListaVendas.java          # extends ListaLigadas
│       └── telas/
│           ├── Tema.java                 # Cores, fontes e estilos
│           ├── TelaInicial.java          # Imagem e botão "Acessar"
│           ├── TelaLogin.java            # Autenticação
│           └── AplicacaoPadaria.java     # Janela principal (sidebar, formulários, abas)
└── test/
    └── padaria/TestesListas.java
```

`ListaProdutos` e `ListaVendas` herdam de `ListaLigadas` e fazem tudo através dos
seus métodos (`adicionaFim`, `pega`, `removePosicao`, `contem`, `tamanho`,
`posicaoValida`, `estaVazio`). Os resultados das buscas e listagens são também
`ListaLigadas`.

## Operações

- Login com controlo de acesso (Dono da Padaria / Funcionário)
- Cadastro de produtos
- Busca por um atributo / por dois atributos combinados
- Alteração de dados (por código)
- Eliminação por posição / por código
- Impressão: todos / por critério / ordenados (bubble sort)
- Registo de vendas
