import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Relatório de Vendas - Abril 2025",
    page_icon="📊",
    layout="wide"
)

# Carregando os dados
df = pd.read_excel("abril25.xlsx")
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# SIDEBAR - Filtros
st.sidebar.header("🔍 Filtros")

vendedores = df['Nome'].dropna().unique().tolist()
tipos = df['Tipo'].dropna().unique().tolist()
situacoes = df['Situação'].dropna().unique().tolist()

filtro_vendedor = st.sidebar.multiselect("Vendedor", vendedores, default=vendedores)
filtro_tipo = st.sidebar.multiselect("Tipo", tipos, default=tipos)
filtro_situacao = st.sidebar.multiselect("Situação", situacoes, default=situacoes)

# Filtro do DataFrame
abril_2025 = df[
    (df['Data'].dt.month == 4) &
    (df['Data'].dt.year == 2025) &
    (df['Nome'].isin(filtro_vendedor)) &
    (df['Tipo'].isin(filtro_tipo)) &
    (df['Situação'].isin(filtro_situacao))
]

st.title("📈 Relatório de Vendas - Abril 2025")

# Verifica se há dados após o filtro
if abril_2025.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
else:
    # MÉTRICAS
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas (R$)", f"{abril_2025['Valor total'].sum():,.2f}")
    col2.metric("Itens Vendidos", int(abril_2025['Quantidade'].sum()))
    col3.metric("Vendedores Ativos", abril_2025['Nome'].nunique())

    st.divider()

    # GRÁFICO DE VENDAS DIÁRIAS
    vendas_diarias = abril_2025.groupby('Data')['Valor total'].sum().reset_index()
    fig_diario = px.bar(
        vendas_diarias,
        x='Data',
        y='Valor total',
        labels={'Valor total': 'Total Vendido (R$)', 'Data': 'Dia'},
        title="📅 Vendas Diárias - Abril 2025",
        text_auto='.2s'
    )
    st.plotly_chart(fig_diario, use_container_width=True)

    # GRÁFICO DE VENDAS POR VENDEDOR E TIPO
    vendas_por_vendedor_tipo = abril_2025.groupby(['Nome', 'Tipo'])['Valor total'].sum().reset_index()
    totais = vendas_por_vendedor_tipo.groupby('Nome')['Valor total'].sum().sort_values(ascending=False).reset_index()
    vendedores_ordenados = totais['Nome'].tolist()

    fig_vendedores = px.bar(
        vendas_por_vendedor_tipo,
        x='Nome',
        y='Valor total',
        color='Tipo',
        text_auto='.2s',
        title="👤 Vendas por Vendedor (Empilhado por Tipo)",
        labels={'Valor total': 'Total Vendido (R$)', 'Nome': 'Vendedor'},
        category_orders={'Nome': vendedores_ordenados}
    )
    fig_vendedores.update_layout(barmode='stack', xaxis_tickangle=-45)
    st.plotly_chart(fig_vendedores, use_container_width=True)

    st.divider()

    # TABELA DETALHADA
    st.subheader("📋 Detalhamento das Vendas")
    st.dataframe(abril_2025.sort_values(by='Data'), use_container_width=True)