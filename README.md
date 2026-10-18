# SQL Sales Analytics

Projeto de portfólio para demonstrar modelagem relacional e análise de vendas com SQL e MySQL 8. O esquema organiza clientes, produtos, pedidos e os itens que compõem cada pedido.

## Objetivos

- Praticar consultas analíticas com junções, agregações, CTEs e funções de data.
- Analisar faturamento calculado, evolução mensal, produtos, clientes e ticket médio.
- Documentar o modelo e os critérios das métricas de forma reproduzível.

## Tecnologias

- MySQL 8.0
- SQL
- Visual Studio Code com SQLTools

## Estrutura do repositório

```text
.
├── .gitignore
├── data/
│   └── sql_sales_analytics_backup_2026.sql  # Backup local, ignorado pelo Git
├── database/
│   └── estrutura.sql                       # Estrutura das quatro tabelas
├── docs/
│   ├── metricas-e-reproducao.md
│   └── modelo-relacional.md
└── queries/
    ├── 01-faturamento-geral.sql
    ├── 02-vendas-por-periodo.sql
    ├── 03-produtos-mais-vendidos.sql
    ├── 04-clientes-maiores-compras.sql
    └── 05-ticket-medio.sql
```

## Modelo e dados

O modelo contém as tabelas `clientes`, `produtos`, `pedidos` e `itens_pedido`. O backup local analisado contém 1.000 clientes, 600 produtos, 2.000 pedidos e 5.000 itens de pedido. Esses totais descrevem a quantidade de registros encontrada no arquivo, não resultados de vendas. O backup não é incluído no Git; consulte a seção de segurança e reprodução.

Os relacionamentos, colunas e chaves estão descritos em [`docs/modelo-relacional.md`](docs/modelo-relacional.md). O arquivo [`database/estrutura.sql`](database/estrutura.sql) corresponde às definições de tabela do backup; os valores de `AUTO_INCREMENT` do dump refletem seu estado no momento da exportação.

## Consultas analíticas

Todas as consultas consideram exclusivamente pedidos cujo `status_pedido` seja `'Concluido'`.

| Arquivo | Análise |
| --- | --- |
| `01-faturamento-geral.sql` | Pedidos concluídos com itens, unidades e valor calculado |
| `02-vendas-por-periodo.sql` | Pedidos concluídos agrupados por mês |
| `03-produtos-mais-vendidos.sql` | Produtos classificados por unidades em pedidos concluídos |
| `04-clientes-maiores-compras.sql` | Clientes classificados pelo valor de pedidos concluídos |
| `05-ticket-medio.sql` | Média do valor calculado por pedido concluído com itens |

Os valores monetários são calculados pela soma de `quantidade * preco_unitario` em `itens_pedido`. O preço utilizado é o registrado no item, não o preço atual do cadastro de produtos. As consultas não contêm comandos de criação, alteração ou exclusão de dados.

## Como utilizar

1. Utilize uma instância MySQL 8.0 com o esquema compatível com `database/estrutura.sql` e dados autorizados para análise.
2. Configure a conexão no SQLTools localmente. Não salve credenciais no repositório.
3. Abra a consulta desejada em `queries/`, leia os comentários e execute-a no seu ambiente.

Este trabalho não executa as consultas nem importa o backup. `database/estrutura.sql` é documentação do esquema, não foi executado nesta organização. O backup local está listado no `.gitignore` e não deve ser publicado sem revisão e autorização adequadas.

## Segurança e reprodução

O backup contém registros de clientes com nomes e localização em nível de cidade/estado. Embora não tenham sido encontrados campos de contato ou credenciais no esquema, não é possível confirmar apenas pelo arquivo se os dados são fictícios ou se há autorização para divulgação. Por segurança, o backup está excluído do controle de versão. Use dados sintéticos ou anonimizados e autorizados se precisar compartilhar uma cópia reproduzível.

Para reproduzir as análises em outro ambiente, são necessários MySQL 8.0, a estrutura documentada e dados de teste autorizados. As métricas usam o status `'Concluido'`, observado nos dados do backup. Veja [`docs/metricas-e-reproducao.md`](docs/metricas-e-reproducao.md) para detalhes e limitações.
