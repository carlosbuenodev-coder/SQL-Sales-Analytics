# Métricas e reprodução

## Critério comum das consultas

As cinco consultas em `queries/` consideram apenas pedidos com `pedidos.status_pedido = 'Concluido'`, valor observado no backup analisado. Pedidos pendentes ou cancelados ficam fora das métricas de vendas. Não foram calculados nem registrados resultados de faturamento nesta documentação.

## Definições das métricas

- **Valor calculado do item:** `itens_pedido.quantidade * itens_pedido.preco_unitario`.
- **Faturamento calculado:** soma do valor dos itens pertencentes a pedidos concluídos.
- **Vendas por período:** soma dos valores dos itens e unidades por mês de `pedidos.data_pedido`, para pedidos concluídos.
- **Produtos mais vendidos:** soma das quantidades por produto em pedidos concluídos; o valor usa o preço unitário registrado no item.
- **Maiores compras por cliente:** soma dos valores dos itens em pedidos concluídos associados ao cliente.
- **Ticket médio:** média do valor total dos pedidos concluídos que possuem itens.

`produtos.preco` representa o preço cadastrado atualmente; não substitui `itens_pedido.preco_unitario` nas consultas, pois este último registra o valor do item do pedido.

## Cobertura observada no backup

A leitura textual do backup identificou estas quantidades de registros: 1.000 em `clientes`, 600 em `produtos`, 2.000 em `pedidos` e 5.000 em `itens_pedido`. Entre os pedidos, o arquivo contém os status `Concluido`, `Cancelado` e `Pendente`. Os números são contagens de linhas de dados do arquivo, não resultados de análise de vendas.

## Reproduzir em outro ambiente

Para reproduzir as consultas são necessários:

1. MySQL 8.0.
2. As quatro tabelas com a estrutura compatível com `database/estrutura.sql`.
3. Dados de teste autorizados que incluam pedidos e itens associados.
4. Uma conexão local configurada no cliente SQL, sem versionar credenciais.

O backup existente foi excluído do Git por conter registros de clientes. O esquema inclui nomes e localização em nível de cidade/estado; não foi possível confirmar pelo arquivo se todos os registros são fictícios ou se há autorização para compartilhamento. Não publique o backup original. Para uma demonstração pública, prefira dados sintéticos ou anonimizados, com autorização e validação antes de incluí-los.

## Escopo do arquivo de estrutura

`database/estrutura.sql` documenta os comandos `CREATE TABLE` e corresponde à estrutura das quatro tabelas do backup. Ele não contém dados de carga. A conferência foi feita pela leitura dos arquivos: nenhum comando SQL foi executado, nenhum dado foi importado e o banco MySQL não foi alterado.
