-- Resume os pedidos por mês de calendário usando a data registrada em pedidos.
-- O valor do período é a soma de quantidade * preço unitário dos itens.
-- Considera somente pedidos com status 'Concluido'.
SELECT
    DATE_FORMAT(p.data_pedido, '%Y-%m') AS periodo,
    COUNT(DISTINCT p.id) AS pedidos_com_itens,
    SUM(ip.quantidade) AS unidades_vendidas,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_calculado
FROM pedidos AS p
INNER JOIN itens_pedido AS ip
    ON ip.pedido_id = p.id
WHERE p.status_pedido = 'Concluido'
GROUP BY DATE_FORMAT(p.data_pedido, '%Y-%m')
ORDER BY periodo;
