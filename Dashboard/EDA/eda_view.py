import streamlit as st
from . import eda_data as dt
import numpy as np

def present_eda():
  st.markdown(
    """
    # Análise exploratória de dados
    """

    """
    Inicialmente, faremos uma análise exploratória dos dados contidos nas Declarações de Óbito do DATASUS.
    Foram selecionados os registros correspondentes às mortes por suicídio, que correspondem aos códigos CID-10 entre X60-X84.

    As principais colunas foram extraídas, formando a tabela abaixo:
    """
  )

  suicide_df = dt.get_suicide_data()
  st.write(suicide_df.head())

  st.markdown(
    """
    ## Análise por data de óbito
    """

    """
    Abaixo, pode-se observar o número de suicídios por data de óbito.
    """
  )

  dt.plot_dtobito()

  st.markdown(
    """
    ## Análise por coluna
    """
  )

  options = np.append(['Selecione uma análise'], ["Idade", "Sexo", "Estado Civil", "Raça/Cor", "Ocupação", "Escolaridade"])
  column = st.selectbox('Selecione uma análise:', options)
  dt.plot_column(column)

  # st.markdown(
  #    """
  #    ## Análise por município de residência
  #    """
  # )

  # plot_codmunres()

  # plot_linha_ii()