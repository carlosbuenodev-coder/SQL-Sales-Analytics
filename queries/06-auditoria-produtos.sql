USE sql_sales_analytics;

-- Auditoria dos produtos cadastrados

SELECT
    COUNT(*) AS total_produtos,
    SUM(CASE
        WHEN nome LIKE '%Portfolio%'
        THEN 1 ELSE 0
    END) AS produtos_genericos,
    SUM(CASE
        WHEN nome NOT LIKE '%Portfolio%'
        THEN 1 ELSE 0
    END) AS produtos_nomeados
FROM produtos;

-- Estrutura da tabela produtos
DESCRIBE produtos;

-- Amostra dos produtos genéricos
SELECT *
FROM produtos
WHERE nome LIKE '%Portfolio%'
LIMIT 10;

-- Auditoria por categoria
SELECT
    categoria,
    COUNT(*) AS total_produtos,
    SUM(
        CASE
            WHEN nome LIKE '%Portfolio%'
            THEN 1 ELSE 0
        END
    ) AS produtos_genericos,
    MIN(preco) AS menor_preco,
    MAX(preco) AS maior_preco,
    ROUND(AVG(preco), 2) AS preco_medio
FROM produtos
GROUP BY categoria
ORDER BY categoria;

-- Verificar estrutura dos itens vendidos
DESCRIBE itens_pedido;

-- Conferir exemplos de vendas
SELECT *
FROM itens_pedido
LIMIT 10;

-- Verificar estrutura dos itens vendidos
DESCRIBE itens_pedido;

-- Conferir exemplos de vendas
SELECT *
FROM itens_pedido
LIMIT 10;

-- Conferir faturamento pelos preços históricos
SELECT
    COUNT(DISTINCT p.id) AS pedidos_concluidos,
    SUM(ip.quantidade) AS unidades_vendidas,
    ROUND(
        SUM(ip.quantidade * ip.preco_unitario),
        2
    ) AS faturamento
FROM pedidos p
INNER JOIN itens_pedido ip
    ON p.id = ip.pedido_id
WHERE p.status_pedido = 'Concluido';