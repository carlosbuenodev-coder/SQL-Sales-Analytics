"""SQL Sales Analytics — Dashboard v2.1 (Streamlit + MySQL).
Copie este arquivo inteiro para dashboard/app.py.
Requer dashboard/conexao.py com conectar_mysql().
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from conexao import conectar_mysql

st.set_page_config(page_title="SQL Sales Analytics", page_icon="📊", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
h1 {font-weight: 750 !important;}
[data-testid="stMetricValue"] {font-size: clamp(1.05rem, 1.8vw, 1.75rem) !important; overflow-wrap: anywhere;}
[data-testid="stMetric"] {background: rgba(127,127,127,.065); padding: 18px; border-radius: 12px; border: 1px solid rgba(127,127,127,.12);}
</style>
""", unsafe_allow_html=True)


def brl(valor):
    """Formata número em reais no padrão brasileiro."""
    return "R$ " + f"{float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor):
    return f"{int(valor or 0):,}".replace(",", ".")


@st.cache_data(ttl=300, show_spinner=False)
def consultar(sql, params=()):
    conexao = conectar_mysql()
    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, params)
        return pd.DataFrame(cursor.fetchall())
    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()


st.title("📊 SQL Sales Analytics")
st.caption("Dashboard de análise de vendas • Python, MySQL, Pandas, Plotly e Streamlit • Dados fictícios")

try:
    # Os anos são carregados do banco, sem valores fixos no código.
    df_anos = consultar("""
        SELECT DISTINCT YEAR(data_pedido) AS ano
        FROM pedidos
        WHERE status_pedido = 'Concluido'
        ORDER BY ano
    """)
    if df_anos.empty:
        st.warning("Não há pedidos concluídos para analisar.")
        st.stop()

    anos = sorted(df_anos["ano"].dropna().astype(int).tolist())
    st.subheader("Filtros")
    f1, f2 = st.columns(2)
    with f1:
        ano_inicial = st.selectbox("Ano inicial", anos, index=0)
    with f2:
        anos_finais = [ano for ano in anos if ano >= ano_inicial]
        ano_final = st.selectbox("Ano final", anos_finais, index=len(anos_finais) - 1)

    st.caption(f"Período selecionado: {ano_inicial} a {ano_final} • Somente pedidos concluídos")

    # Consultas parametrizadas. Preço histórico: itens_pedido.preco_unitario.
    df_resumo = consultar("""
        SELECT COUNT(DISTINCT p.id) AS pedidos,
               COALESCE(SUM(ip.quantidade), 0) AS unidades,
               COALESCE(SUM(ip.quantidade * ip.preco_unitario), 0) AS faturamento
        FROM pedidos p
        JOIN itens_pedido ip ON ip.pedido_id = p.id
        WHERE p.status_pedido = 'Concluido'
          AND YEAR(p.data_pedido) BETWEEN %s AND %s
    """, (ano_inicial, ano_final))

    resumo = df_resumo.iloc[0]
    pedidos = int(resumo["pedidos"])
    unidades = int(resumo["unidades"])
    faturamento = float(resumo["faturamento"])
    ticket = faturamento / pedidos if pedidos else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento", brl(faturamento))
    c2.metric("Pedidos concluídos", numero(pedidos))
    c3.metric("Unidades vendidas", numero(unidades))
    c4.metric("Ticket médio", brl(ticket))

    st.divider()
    st.subheader("📈 Evolução do faturamento mensal")
        
    df_mensal = consultar("""
        SELECT DATE_FORMAT(p.data_pedido, '%Y-%m') AS mes,
               ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) AS faturamento
        FROM pedidos p
        JOIN itens_pedido ip ON ip.pedido_id = p.id
        WHERE p.status_pedido = 'Concluido'
          AND YEAR(p.data_pedido) BETWEEN %s AND %s
        GROUP BY DATE_FORMAT(p.data_pedido, '%Y-%m')
        ORDER BY mes
    """, (ano_inicial, ano_final))

    # Verifica a última data de venda concluída no período selecionado
    df_ultima_venda = consultar("""
        SELECT MAX(p.data_pedido) AS ultima_data
        FROM pedidos p
        WHERE p.status_pedido = 'Concluido'
        AND YEAR(p.data_pedido) BETWEEN %s AND %s
    """, (ano_inicial, ano_final))

    if not df_ultima_venda.empty:
        ultima_data = pd.to_datetime(
            df_ultima_venda.iloc[0]["ultima_data"],
            errors="coerce"
        )

        if pd.notna(ultima_data):
            fim_do_mes = ultima_data + pd.offsets.MonthEnd(0)

            if ultima_data.date() < fim_do_mes.date():
                st.info(
                    f"📅 Período parcial — {ultima_data.strftime('%m/%Y')}: "
                    f"existem vendas registradas somente até "
                    f"{ultima_data.strftime('%d/%m/%Y')}. "
                    "A comparação com meses completos exige cautela."
                )

            if not df_mensal.empty:
                df_mensal["faturamento"] = pd.to_numeric(df_mensal["faturamento"])
                df_mensal["data"] = pd.to_datetime(df_mensal["mes"] + "-01")# Cria uma cópia para exibir somente os meses completos
    df_linha = df_mensal.copy()

    if not df_ultima_venda.empty and pd.notna(ultima_data):
        fim_do_mes = ultima_data + pd.offsets.MonthEnd(0)

        if ultima_data.date() < fim_do_mes.date():
            df_linha = df_linha[
                df_linha["data"].dt.to_period("M")
                != ultima_data.to_period("M")
            ]

    fig_mensal = px.line(
        df_linha,
        x="data",
        y="faturamento",
        markers=True,
        labels={"data": "Mês", "faturamento": "Faturamento (R$)"}
    )
    fig_mensal.update_layout(hovermode="x unified", margin=dict(t=15, b=15))
    fig_mensal.update_traces(hovertemplate="R$ %{y:,.2f}<extra></extra>")
                # Destaca o último mês quando seus dados são parciais
    if not df_ultima_venda.empty and pd.notna(ultima_data):
            fim_do_mes = ultima_data + pd.offsets.MonthEnd(0)

            if ultima_data.date() < fim_do_mes.date():
                mes_parcial = ultima_data.to_period("M").to_timestamp()

                df_parcial = df_mensal[
                    df_mensal["data"].dt.to_period("M")
                    == mes_parcial.to_period("M")
                ]

                if not df_parcial.empty:
                    fig_mensal.add_scatter(
                        x=df_parcial["data"],
                        y=df_parcial["faturamento"],
                        mode="markers",
                        marker=dict(
                            color="orange",
                            size=13,
                            symbol="circle"
                        ),
                        name="Mês parcial",
                        hovertemplate=(
                            "Mês parcial<br>"
                            "Faturamento: R$ %{y:,.2f}"
                            "<extra></extra>"
                        )
                    )
                st.plotly_chart(fig_mensal, use_container_width=True)
            else:
                st.info("Sem vendas no período selecionado.")

    st.divider()

    st.subheader("📊 Comparação anual - janeiro a julho")

    st.caption("Comparação entre períodos equivalentes: "
        "01/01 a 31/07 de cada ano. "
        "Somente pedidos concluídos."
    )

    df_anual = consultar("""
        SELECT YEAR(p.data_pedido) AS ano,
               COUNT(DISTINCT p.id) AS pedidos,
               ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) AS faturamento
        FROM pedidos p
        JOIN itens_pedido ip ON ip.pedido_id = p.id
        WHERE p.status_pedido = 'Concluido'
          AND YEAR(p.data_pedido) BETWEEN %s AND %s
          AND MONTH(p.data_pedido) BETWEEN 1 AND 7
        GROUP BY YEAR(p.data_pedido)
        ORDER BY ano
    """, (ano_inicial, ano_final))

    if not df_anual.empty:
        df_anual["faturamento"] = pd.to_numeric(df_anual["faturamento"])
        df_anual["ano"] = df_anual["ano"].astype(int)
        df_anual["variacao_pct"] = df_anual["faturamento"].pct_change() * 100
        esquerda, direita = st.columns([1.5, 1])
        with esquerda:
            df_anual["ano_rotulo"] = df_anual["ano"].astype(str)
            fig_anual = px.bar(df_anual, x="ano_rotulo", y="faturamento",
                               labels={"ano_rotulo": "Ano", "faturamento": "Faturamento (R$)"},
                               text="faturamento")
            fig_anual.update_xaxes(type="category", categoryorder="array",
                                   categoryarray=df_anual["ano_rotulo"].tolist())
            fig_anual.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
            fig_anual.update_layout(margin=dict(t=25, b=10), xaxis_title="Ano")
            st.plotly_chart(fig_anual, use_container_width=True)
        with direita:
            st.markdown("**Variação de faturamento em relação ao ano anterior**")
            if len(df_anual) < 2:
                st.info("Selecione pelo menos dois anos para comparar.")
            else:
                for i in range(1, len(df_anual)):
                    atual = df_anual.iloc[i]
                    anterior = df_anual.iloc[i - 1]
                    variacao = atual["variacao_pct"]
                    if pd.notna(variacao):
                        st.metric(f"{int(anterior['ano'])} → {int(atual['ano'])}",
                                  brl(atual["faturamento"]),
                                  delta=f"{variacao:+.2f}%")
                    else:
                        st.write(f"{int(anterior['ano'])} → {int(atual['ano'])}: sem base para variação")
            st.caption("Comparação anual: janeiro a julho de cada ano, considerando somente pedidos concluídos.")

    # Comparação justa entre períodos equivalentes (ano contra ano, mesmo corte de data).
    # Usa a última data disponível no ano mais recente da seleção, não a data do computador
    if len(df_anual) >= 2:
        st.markdown("**Comparação entre períodos equivalentes**")
        ano_recente = int(df_anual["ano"].max())
        ano_anterior = ano_recente - 1
        if ano_anterior in df_anual["ano"].values:
            df_corte = consultar("""
                SELECT MAX(DATE(data_pedido)) AS ultima_data
                FROM pedidos
                WHERE status_pedido = 'Concluido' AND YEAR(data_pedido) = %s
            """, (ano_recente,))
            ultima_data = pd.to_datetime(df_corte.iloc[0]["ultima_data"])
            if pd.notna(ultima_data):
                mes_corte, dia_corte = int(ultima_data.month), int(ultima_data.day)
                # Comparar até o mesmo mês/dia em ambos os anos; 29/02 ajusta para 28/02.
                dia_anterior = min(dia_corte, pd.Period(f"{ano_anterior}-{mes_corte:02d}").days_in_month)
                limite_atual = f"{ano_recente}-{mes_corte:02d}-{dia_corte:02d}"
                limite_anterior = f"{ano_anterior}-{mes_corte:02d}-{dia_anterior:02d}"
                df_equivalente = consultar("""
                    SELECT YEAR(p.data_pedido) AS ano,
                           ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) AS faturamento
                    FROM pedidos p
                    JOIN itens_pedido ip ON ip.pedido_id = p.id
                    WHERE p.status_pedido = 'Concluido'
                      AND ((p.data_pedido >= %s AND p.data_pedido < DATE_ADD(%s, INTERVAL 1 DAY))
                        OR (p.data_pedido >= %s AND p.data_pedido < DATE_ADD(%s, INTERVAL 1 DAY)))
                    GROUP BY YEAR(p.data_pedido)
                """, (f"{ano_anterior}-01-01", limite_anterior,
                      f"{ano_recente}-01-01", limite_atual))
                valores = {int(linha["ano"]): float(linha["faturamento"])
                           for _, linha in df_equivalente.iterrows()}
                valor_anterior = valores.get(ano_anterior, 0.0)
                valor_recente = valores.get(ano_recente, 0.0)
                eq1, eq2, eq3 = st.columns(3)
                eq1.metric(f"{ano_anterior} até {dia_anterior:02d}/{mes_corte:02d}", brl(valor_anterior))
                eq2.metric(f"{ano_recente} até {dia_corte:02d}/{mes_corte:02d}", brl(valor_recente))
                if valor_anterior > 0:
                    diferenca = (valor_recente / valor_anterior - 1) * 100
                    eq3.metric("Variação comparável", f"{diferenca:+.2f}%")
                else:
                    eq3.metric("Variação comparável", "Sem base")
                st.caption("Comparação de 1º de janeiro até o mesmo dia/mês de cada ano, usando a última data com pedido concluído no ano mais recente. Valores fictícios.")
        else:
            st.info("Não há ano imediatamente anterior para comparar períodos equivalentes.")

    st.divider()
    st.subheader("🏆 Produtos e categorias")
    col_prod, col_cat = st.columns(2)

    df_produtos = consultar("""
        SELECT pr.id AS produto_id, pr.nome AS produto,
               ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) AS faturamento
        FROM pedidos p
        JOIN itens_pedido ip ON ip.pedido_id = p.id
        JOIN produtos pr ON pr.id = ip.produto_id
        WHERE p.status_pedido = 'Concluido'
          AND YEAR(p.data_pedido) BETWEEN %s AND %s
        GROUP BY pr.id, pr.nome
        ORDER BY faturamento DESC
        LIMIT 10
    """, (ano_inicial, ano_final))

    with col_prod:
        st.markdown("**Top 10 produtos por faturamento**")
        if not df_produtos.empty:
            df_produtos["faturamento"] = pd.to_numeric(df_produtos["faturamento"])
            # Inclui o ID para diferenciar nomes eventualmente repetidos.
            df_produtos["rotulo"] = df_produtos["produto"] + " (#" + df_produtos["produto_id"].astype(str) + ")"
            fig_prod = px.bar(df_produtos.sort_values("faturamento"),
                              x="faturamento", y="rotulo", orientation="h",
                              labels={"faturamento": "Faturamento (R$)", "rotulo": "Produto"})
            fig_prod.update_layout(margin=dict(t=10, b=10), yaxis_title=None)
            st.plotly_chart(fig_prod, use_container_width=True)
        else:
            st.info("Nenhum produto vendido no período.")

    # Esta consulta pressupõe a coluna 'categoria' na tabela produtos.
    # Se o nome da coluna for diferente, ajuste somente pr.categoria.
    with col_cat:
        st.markdown("**Faturamento por categoria**")
        try:
            df_categorias = consultar("""
                SELECT COALESCE(NULLIF(TRIM(pr.categoria), ''), 'Sem categoria') AS categoria,
                       ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) AS faturamento
                FROM pedidos p
                JOIN itens_pedido ip ON ip.pedido_id = p.id
                JOIN produtos pr ON pr.id = ip.produto_id
                WHERE p.status_pedido = 'Concluido'
                  AND YEAR(p.data_pedido) BETWEEN %s AND %s
                GROUP BY COALESCE(NULLIF(TRIM(pr.categoria), ''), 'Sem categoria')
                ORDER BY faturamento DESC
            """, (ano_inicial, ano_final))
            if not df_categorias.empty:
                df_categorias["faturamento"] = pd.to_numeric(df_categorias["faturamento"])
                fig_cat = px.bar(df_categorias.sort_values("faturamento"),
                                 x="faturamento", y="categoria", orientation="h",
                                 labels={"faturamento": "Faturamento (R$)", "categoria": "Categoria"})
                fig_cat.update_layout(margin=dict(t=10, b=10), yaxis_title=None)
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.info("Nenhuma categoria no período.")
        except Exception as erro_categoria:
            st.warning("Não foi possível consultar categorias. Confira se a tabela produtos possui a coluna 'categoria'.")
            st.caption(str(erro_categoria))

    st.divider()
    st.caption("Fonte: MySQL • Faturamento calculado com itens_pedido.quantidade × itens_pedido.preco_unitario (preços históricos). Consultas somente de leitura.")
    if st.button("🔄 Atualizar dados"):
        consultar.clear()
        st.rerun()

except Exception as erro:
    st.error("Não foi possível carregar o dashboard. Confira a conexão com o MySQL e os nomes das tabelas/colunas.")
    st.exception(erro)
