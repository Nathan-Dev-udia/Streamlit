# 📊 Relatório de Vendas - Abril 2025 (Streamlit)

## Descrição do Projeto
Este projeto surgiu como alternativa ao Power BI para a criação de relatórios de vendas interativos e compartilháveis.  
Embora inicialmente eu utilizasse o Power BI, sua versão gratuita possui limitações para apresentação e compartilhamento dos dashboards. Por isso, optei por criar este projeto em **Streamlit**, permitindo:  

- Exibir os relatórios de forma interativa;  
- Filtrar os dados por vendedor, tipo e situação da venda;  
- Visualizar métricas e gráficos diretamente em um navegador ou notebook conectado a uma TV;  
- Fazer apresentações em tela cheia com facilidade (F11).  

O arquivo Excel usado (`abril25.xlsx`) contém dados reais de vendas, porém as colunas de **CNPJ** e **vendedores** foram alteradas para preservar a privacidade.

---

## Funcionalidades

- **Filtros interativos:** selecione vendedor, tipo e situação da venda.  
- **Métricas principais:** total vendido, itens vendidos e número de vendedores ativos.  
- **Gráficos interativos:**  
  - Vendas diárias em barra;  
  - Vendas por vendedor empilhadas por tipo.  
- **Tabela detalhada:** visualização completa dos dados filtrados.  

---

## Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) – criação do dashboard web interativo  
- [Pandas](https://pandas.pydata.org/) – manipulação e filtragem de dados  
- [Plotly](https://plotly.com/python/) – gráficos interativos  
- [LibreOffice / Excel] – preparação da base de dados  

---

## Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

2. Instale as dependencias:
pip install streamlit pandas plotly openpyxl

3. Execute o dashboard:
streamlit run relatvenda.py
