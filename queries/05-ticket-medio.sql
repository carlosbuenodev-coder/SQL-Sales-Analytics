-- Calcula o ticket médio como a média do total calculado de cada pedido com itens.
-- A CTE primeiro consolida os itens por pedido; a consulta externa tira a média
-- desses totais. Pedidos sem itens não entram no cálculo. Somente pedidos
-- com status 'Concluido' são considerados.
WITH total_por_pedido AS (
    SELECT
        p.id AS pedido_id,
        SUM(ip.quantidade * ip.preco_unitario) AS valor_pedido
    FROM pedidos AS p
    INNER JOIN itens_pedido AS ip
        ON ip.pedido_id = p.id
    WHERE p.status_pedido = 'Concluido'
    GROUP BY p.id
)
SELECT
    COUNT(*) AS pedidos_com_itens,
    AVG(valor_pedido) AS ticket_medio_calculado
FROM total_por_pedido;

-- RESULTADOS DA EXECUCAO
-- Pedidos concluidos com itens: 1610
-- Faturamento total: R$ 17.471.526,15
-- Ticket medio: R$ 10.851,88
--
-- O ticket medio representa o valor medio
-- dos pedidos concluidos com itens.