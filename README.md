# Padaria

Sistema de Gestão de Padaria — Trabalho Prático 1 de Algoritmos e Estruturas de Dados
(ISUTC — Engenharia Informática e de Telecomunicações).

- **Linguagem:** Java (8 ou superior)
- **Estrutura de dados:** Lista Duplamente Ligada (`ListaLigadas`), usada para produtos e vendas
- **Interface gráfica:** Swing
- **Dependências:** nenhuma além da biblioteca padrão do Java

## Como executar

No Eclipse: *File → Import → Existing Projects into Workspace*, escolher esta pasta
e correr `SistemaPadaria`.

Na linha de comandos, a partir da raiz do projecto:

```bash
javac -encoding UTF-8 -d bin -sourcepath src src/listas_duplamente_ligadas/SistemaPadaria.java
java -cp bin listas_duplamente_ligadas.SistemaPadaria
```

Utilizadores de teste:

| Utilizador    | Senha     | Perfil          |
|---------------|-----------|-----------------|
| `dono`        | `dono123` | Dono da Padaria |
| `funcionario` | `func123` | Funcionário     |

O Funcionário não vê as operações de cadastrar, alterar e eliminar.

## Testes

```bash
javac -encoding UTF-8 -d bin -sourcepath src:test test/listas_duplamente_ligadas/TestesListas.java
java -cp bin listas_duplamente_ligadas.TestesListas
```
(No Windows, `src;test` em vez de `src:test`.)

## Estrutura do projecto

```
Padaria/
├── src/
│   ├── imagens/
│   │   └── fundo_inicial.png          # Imagem da tela inicial
│   └── listas_duplamente_ligadas/
│       ├── IntefaceGeral.java         # Operações da lista
│       ├── No.java                    # Nó (anterior, elemento, próximo)
│       ├── ListaLigadas.java          # Lista duplamente ligada (base de tudo)
│       ├── ListaProdutos.java         # extends ListaLigadas: cadastro, busca, eliminação, ordenação
│       ├── ListaVendas.java           # extends ListaLigadas: vendas e totais
│       ├── Produto.java               # Elemento da lista de produtos (+ enum Atributo)
│       ├── Venda.java                 # Elemento da lista de vendas
│       ├── Utilizador.java
│       ├── SistemaPadaria.java        # main(), configuração (utilizadores, permissões) e tema visual
│       ├── TelaInicial.java           # Imagem e botão "Acessar"
│       ├── TelaLogin.java             # Autenticação
│       └── AplicacaoPadaria.java      # Janela principal (sidebar, formulários, abas)
└── test/
    └── listas_duplamente_ligadas/TestesListas.java
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
