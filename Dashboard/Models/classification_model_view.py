import streamlit as st
from . import classification_model_data as dt
import numpy as np

def present_classification_model():
  st.markdown(
    """
    # Modelos de Classificação
    """

    
  )
  analysis = st.radio("Qual modelo?",('Mediana Nacional', 'Clusters do SatScan'))
  if analysis == "Mediana Nacional":
    st.markdown(
      """
      ## Modelo da Mediana Nacional
      """
    )
  else:
    st.markdown(
      """
      ## Modelo de Clusters do SatScan
      """
    )
  
  options = np.append(['Selecione um modelo'], ["Naive Bayes", "Regressão Logística", "Random Forest", "SVC (Linear)", "SVC (RBF)"])
  model = st.selectbox('Selecione um modelo:', options)

  if analysis == "Mediana Nacional":
    dt.highest_rates_model(model)
  else:
    dt.satscan_model(model)