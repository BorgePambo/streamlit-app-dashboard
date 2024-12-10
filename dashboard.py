import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout='wide')

#faturamento por unidade
#tipo de produto mais vendido
#desempenho na forma de pagamento
#como estão as avaliações das filiais

st.header('Dashboard de Perfomance de Venda')
df = pd.read_csv('data/supermarket_sales.csv', sep=';', decimal=',')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

df['Month'] = df['Date'].apply(lambda x: str(x.year) + '-' + str(x.month))
month = st.sidebar.selectbox('Mes', df['Month'].unique())

df_filtered = df[df['Month'] == month]
df_filtered

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)
col6 = st.columns(1)

fig_date = px.bar(df_filtered, x='Date', y='Total', color='City', title='Faturamento por Dia')
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x='Date', y='Product line', color='City', 
                    title='Faturamento por Tipo de Produto',
                    orientation='h')
col2.plotly_chart(fig_prod, use_container_width=True)


city_total = df_filtered.groupby('City')[['Total']].sum().reset_index()
fig_city = px.bar(df_filtered, x='City', y='Total',  
                  title='Faturamento por Filial',)
col3.plotly_chart(fig_city, use_container_width=True)


fig_tipo_pag = px.pie(df_filtered, values='Total', names='Payment',  
                  title='Faturamento por Tipo de Pagamento',)
col4.plotly_chart(fig_tipo_pag, use_container_width=True )



city_total = df_filtered.groupby('City')[['Rating']].mean().reset_index()
fig_rating = px.bar(df_filtered, x='Rating', y='City', title='Avaliação')

fig_rating.update_layout(
    title_text='Avaliação',  # Título do gráfico
    title_x=0.5,  # Posição horizontal do título (0.5 centraliza)
    title_xanchor='center'  # Ancorar o título no centro
)

col5.plotly_chart(fig_rating, use_container_width=True)


product_metric = df_filtered.groupby('Product line').agg(
    maximo=('Total', 'max'),
    minimo=('Total', 'min'),
    média=('Total', 'mean'),
    soma=('Total', 'sum')
).reset_index()

st.dataframe(product_metric)
