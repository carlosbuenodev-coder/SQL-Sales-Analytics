-- Classifica produtos pela quantidade total registrada nos itens dos pedidos.
-- O valor é calculado pelo preço unitário armazenado no item, não pelo preço
-- atual do cadastro do produto. Considera somente pedidos concluídos.
SELECT
    pr.id AS produto_id,
    pr.nome AS produto,
    pr.categoria,
    SUM(ip.quantidade) AS unidades_vendidas,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_calculado
FROM produtos AS pr
INNER JOIN itens_pedido AS ip
    ON ip.produto_id = pr.id
INNER JOIN pedidos AS p
    ON p.id = ip.pedido_id
WHERE p.status_pedido = 'Concluido'
GROUP BY pr.id, pr.nome, pr.categoria
ORDER BY unidades_vendidas DESC, produto ASC;
