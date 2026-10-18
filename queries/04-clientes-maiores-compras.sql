-- Lista clientes pelo valor total calculado dos itens associados aos seus pedidos.
-- COUNT(DISTINCT) evita contar o mesmo pedido mais de uma vez quando ele possui
-- vários itens. Considera somente pedidos com status 'Concluido'.
SELECT
    c.id AS cliente_id,
    c.nome AS cliente,
    c.cidade,
    c.estado,
    COUNT(DISTINCT p.id) AS pedidos_com_itens,
    SUM(ip.quantidade * ip.preco_unitario) AS valor_total_calculado
FROM clientes AS c
INNER JOIN pedidos AS p
    ON p.cliente_id = c.id
INNER JOIN itens_pedido AS ip
    ON ip.pedido_id = p.id
WHERE p.status_pedido = 'Concluido'
GROUP BY c.id, c.nome, c.cidade, c.estado
ORDER BY valor_total_calculado DESC, cliente ASC;
