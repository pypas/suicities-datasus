import streamlit as st
from eda_data import *

"""
# Análise exploratória de dados
"""

"""
Inicialmente, faremos uma análise exploratória dos dados contidos nas Declarações de Óbito do DATASUS.
Foram selecionados os registros correspondentes às mortes por suicídio, que correspondem aos códigos CID-10 entre X60-X84.

As principais colunas foram extraídas, formando a tabela abaixo:
"""
suicide_df = get_suicide_data()
st.write(suicide_df.head())

"""
## Análise por data de óbito
"""

"""
Abaixo, pode-se observar o número de suicídios por data de óbito.
"""
plot_dtobito()



"""
## Análise por coluna
"""

options = np.append(['Selecione uma análise'], ["Idade", "Sexo", "Estado Civil", "Raça/Cor", "Ocupação", "Escolaridade"])
column = st.selectbox('Selecione uma análise:', options)
plot_column(column)

# """
# ## Análise por município de residência
# """

# plot_codmunres()

#plot_linha_ii()