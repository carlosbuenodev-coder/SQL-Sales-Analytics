# SQL Sales Analytics

Projeto de portfólio de análise de vendas com **MySQL 8**, **SQL**, **Python**, **Pandas**, **Plotly** e **Streamlit**. Os dados são fictícios.

## Objetivo

Explorar vendas concluídas, identificar tendências, comparar períodos e apresentar indicadores de negócio por meio de um dashboard interativo.

## Funcionalidades

- Filtros por ano inicial e final.
- Faturamento, quantidade de pedidos, unidades vendidas e ticket médio.
- Evolução mensal do faturamento.
- Comparação anual e variação percentual.
- Comparação entre períodos equivalentes (ano anterior x ano atual, até a última data com pedido concluído).
- Top 10 produtos e faturamento por categoria.

> Atenção: a comparação de anos completos com anos parciais pode induzir a interpretações incorretas. Utilize a seção de períodos equivalentes para uma análise mais justa. A comparação é feita com base na última data disponível nos dados, não necessariamente na data de hoje.

## Estrutura sugerida

```text
SQL-Sales-Analytics/
├── dashboard/
│   ├── app.py
│   └── conexao.py
├── database/
├── data/
├── docs/
│   └── imagens/
├── queries/
├── .gitignore
├── .env.example
├── requirements.txt
└── README.md
```

## Como executar localmente

1. Instale Python e MySQL e configure o banco de dados com os scripts SQL do projeto.
2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

4. Configure as variáveis de ambiente `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` e `MYSQL_DATABASE`. Consulte `.env.example`. O arquivo `dashboard/conexao.py` deve ler essas variáveis; há um exemplo opcional no kit (`conexao_segura_exemplo.py`).
5. Inicie o aplicativo:

```powershell
python -m streamlit run dashboard/app.py
```

6. Acesse `http://localhost:8501`.

## Regras de negócio

- Apenas pedidos com `status_pedido = 'Concluido'` entram nos indicadores.
- O faturamento utiliza `itens_pedido.quantidade * itens_pedido.preco_unitario`, preservando o preço histórico de cada venda.
- O ticket médio é faturamento dividido pela quantidade de pedidos concluídos.
- O catálogo contém nomes genéricos `Produto Portfolio` ainda em revisão; nomes sugeridos de marcas e modelos não devem ser tratados como verificados nem aplicados automaticamente.

## Evidências visuais

Adicione capturas de tela do dashboard em `docs/imagens/`, sem exibir senhas ou dados pessoais. Sugestões: `visao-geral.png`, `comparacao-anual.png` e `produtos-categorias.png`.

## Segurança

**Nunca envie credenciais, `.env`, dumps privados, backups, `.venv` ou dados sensíveis ao GitHub.** Verifique o histórico do Git: o `.gitignore` não apaga segredos que já foram versionados. Se alguma senha já foi publicada, troque-a no MySQL.

## Próximos passos

- Revisar e validar individualmente o catálogo de produtos.
- Completar documentação do modelo relacional e das consultas SQL.
- Publicar capturas de tela e resultados reproduzíveis.
