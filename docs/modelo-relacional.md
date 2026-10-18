# Modelo relacional

Este documento descreve as quatro tabelas definidas em `database/estrutura.sql` e conferidas com as definições de tabela presentes no backup local. Nenhuma coluna foi acrescentada à documentação além das que constam no esquema.

## Tabelas e colunas

### `clientes`

| Coluna | Tipo | Regra declarada |
| --- | --- | --- |
| `id` | `int` | Chave primária, auto incremento, obrigatório |
| `nome` | `varchar(100)` | Obrigatório |
| `cidade` | `varchar(100)` | Opcional |
| `estado` | `char(2)` | Opcional |
| `data_cadastro` | `date` | Opcional |

### `produtos`

| Coluna | Tipo | Regra declarada |
| --- | --- | --- |
| `id` | `int` | Chave primária, auto incremento, obrigatório |
| `nome` | `varchar(100)` | Obrigatório |
| `categoria` | `varchar(50)` | Opcional |
| `preco` | `decimal(10,2)` | Obrigatório |

### `pedidos`

| Coluna | Tipo | Regra declarada |
| --- | --- | --- |
| `id` | `int` | Chave primária, auto incremento, obrigatório |
| `cliente_id` | `int` | Obrigatório; chave estrangeira para `clientes.id` |
| `data_pedido` | `date` | Obrigatório |
| `status_pedido` | `varchar(20)` | Obrigatório; padrão `'Pendente'` |

### `itens_pedido`

| Coluna | Tipo | Regra declarada |
| --- | --- | --- |
| `id` | `int` | Chave primária, auto incremento, obrigatório |
| `pedido_id` | `int` | Obrigatório; chave estrangeira para `pedidos.id` |
| `produto_id` | `int` | Obrigatório; chave estrangeira para `produtos.id` |
| `quantidade` | `int` | Obrigatório |
| `preco_unitario` | `decimal(10,2)` | Obrigatório |

As quatro tabelas usam InnoDB, conjunto de caracteres `utf8mb4` e collation `utf8mb4_0900_ai_ci`.

## Relacionamentos

```text
clientes (1) ──── (N) pedidos (1) ──── (N) itens_pedido (N) ──── (1) produtos
```

- `pedidos.cliente_id` referencia `clientes.id`: um pedido pertence a um cliente; um cliente pode ter vários pedidos.
- `itens_pedido.pedido_id` referencia `pedidos.id`: um item pertence a um pedido; um pedido pode ter vários itens.
- `itens_pedido.produto_id` referencia `produtos.id`: um item referencia um produto; um produto pode aparecer em vários itens.
- `itens_pedido` associa pedidos a produtos e registra quantidade e preço unitário do item.

## Integridade e observações

- `id` é a chave primária de cada tabela.
- As colunas de chave estrangeira têm índices declarados no esquema.
- Não há constraint de unicidade declarada para pares de produto e pedido.
- Não há ações de exclusão ou atualização em cascata declaradas nas chaves estrangeiras.
- `produtos.preco` é o preço cadastrado no produto. As consultas de valores de venda usam `itens_pedido.preco_unitario`.
- A estrutura de colunas, chaves e índices de `database/estrutura.sql` corresponde ao DDL das quatro tabelas no backup. Os valores de `AUTO_INCREMENT` presentes no dump são estado da exportação, não novas colunas ou relacionamentos.

## Cobertura de registros no backup analisado

O arquivo local de backup contém registros para todas as quatro tabelas: 1.000 em `clientes`, 600 em `produtos`, 2.000 em `pedidos` e 5.000 em `itens_pedido`. O backup é ignorado pelo Git e esses totais não incluem informação pessoal individualizada.
