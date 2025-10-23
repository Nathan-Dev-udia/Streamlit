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

# Vendedor
vendedores = sorted(df['Nome'].dropna().unique().tolist())
vendedores.insert(0, "Todos")
vendedor_selecionado = st.sidebar.selectbox("Vendedor", vendedores)

# Tipo
tipos = sorted(df['Tipo'].dropna().unique().tolist())
tipos.insert(0, "Todos")
tipo_selecionado = st.sidebar.selectbox("Tipo", tipos)

# Situação
situacoes = sorted(df['Situação'].dropna().unique().tolist())
situacoes.insert(0, "Todos")
situacao_selecionada = st.sidebar.selectbox("Situação", situacoes)

# Aplicar filtros
abril_2025 = df[
    (df['Data'].dt.month == 4) &
    (df['Data'].dt.year == 2025)
]

if vendedor_selecionado != "Todos":
    abril_2025 = abril_2025[abril_2025['Nome'] == vendedor_selecionado]

if tipo_selecionado != "Todos":
    abril_2025 = abril_2025[abril_2025['Tipo'] == tipo_selecionado]

if situacao_selecionada != "Todos":
    abril_2025 = abril_2025[abril_2025['Situação'] == situacao_selecionada]

# TÍTULO
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