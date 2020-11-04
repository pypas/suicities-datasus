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
    ## Análises por coluna
    """
  )

  options = np.append(['Selecione uma análise'], ["Data de Óbito", "Causa Básica", "Linha II", "Município de Residência","Idade", "Sexo", "Estado Civil", "Raça/Cor", "Ocupação", "Escolaridade"])
  column = st.selectbox('Selecione uma análise:', options)
  

  if column == "Data de Óbito":
    st.markdown(
      """
      Abaixo, pode-se observar o número de suicídios por data de óbito.
      """
    )
  elif column == "Causa Básica":
    st.markdown(
      """
      A coluna CAUSABAS da declaração de óbito corresponde à doença ou lesão que iniciou a cadeia de acontecimentos patológicos que conduziram diretamente à morte, ou as circunstâncias do acidente ou violência que produziram a lesão fatal.
      """
    )
  elif column == "Linha II":
    st.markdown(
      """
      A linha II da declaração de óbito corresponde às condições mórbidas pré-existentes no indivíduo e sem relação direta com sua morte.
      """
    )
  dt.plot_column(column)