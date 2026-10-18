-- Faturamento calculado a partir dos itens registrados nos pedidos.
-- Cada linha de itens_pedido representa um produto, quantidade e preço unitário.
-- Considera somente pedidos concluídos. O resultado é calculado ao executar.
SELECT
    COUNT(DISTINCT p.id) AS pedidos_com_itens,
    SUM(ip.quantidade) AS unidades_vendidas,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_calculado
FROM pedidos AS p
INNER JOIN itens_pedido AS ip
    ON ip.pedido_id = p.id
WHERE p.status_pedido = 'Concluido';
