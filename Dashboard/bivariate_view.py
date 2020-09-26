import streamlit as st
import numpy as np
import pandas as pd
import time
from splot.esda import moran_scatterplot, lisa_cluster
from bivariate_data import compute_weights, get_dataset, get_disease_dataset, merge_dataset_disease, moran_local_bv

"""
# Bivariate Moran\'s I
"""

"""
O Bivariate Moran's I é uma estatística calculada para medir a **correlação espacial** entre duas grandezas.

Esse cálculo é feito tomando o valor de uma variável dependente $x$ em uma região $r_1$, e calculando uma função de agregação de
uma variável $y$ nas regiões vizinhas da região $r_1$. Essa função costuma ser a **média aritmética**, e chamamos de $lag(y)$.

Após esse cálculo para cada região $r$ do mapa, calcula-se uma reta de regressão que passa pelos pontos $(x_r, 
lag(y_r))$ de cada região. O coeficiente dessa reta é o **Moran's I**, e representa o quanto $lag(y_r)$ aumenta com $x_r$.
"""

"""
## **Cálculo para doenças e suicídio**
"""

"""
Neste dashboard, apresentamos o mapa do Brasil subdividido em seus municípios.

A variável dependente é uma **doença do DATASUS**, e pode ser escolhida por você!

A variável-alvo é a **taxa de suicídios por 100.000 habitantes**.

Os municípios são coloridos de acordo com o grau de correlação espacial entre a variável escolhida e 
a taxa de suicídios nos municípios adjacentes, para cada município do mapa, conforme explicado na legenda abaixo:
"""

st.markdown(
    '<ul>'
        '<li>HH (<i>High-High</i>): em <span style="color:red;"><b>vermelho</b></span>, representa um município onde a taxa da doença selecionada e a taxa de suicídios na vizinhança são altos.</li>'
        '<li>LL (<i>Low-Low</i>): em <span style="color:blue;"><b>azul</b></span>, representa um município onde a taxa da doença selecionada e a taxa de suicídios na vizinhança são baixos.</li>'
    '</ul>', unsafe_allow_html=True
)

st.markdown(
    '<p>Os municípios HL (<i>High-Low</i>) e LH (<i>Low-High</i>) são mostrados em <span style="color:gray;"><b>cinza</b></span>, pois não apresentam uma concordância '
    'entre a taxa da doença apresentada no município e a taxa de suicídio nas redondezas desse município.</p>', unsafe_allow_html=True
)

"""
## **Mapa de correlação**
"""

def moran_scatterplt(moran_loc_bv):
    fig, ax = moran_scatterplot(moran_loc_bv, p=0.05)
    ax.set_xlabel('Suicides')
    ax.set_ylabel('Spatial lag of mental disorder')
    st.pyplot(fig)

def moran_map(moran_loc_bv, dataset):
    fig = lisa_cluster(moran_loc_bv, dataset, p=0.05, figsize=(9,9))
    st.pyplot(fig)

compute_weights()
dt = get_dataset()

selected_disease = st.selectbox(
    'Selecione uma doença:',
    ['Selecione uma doença', 'Artrose'])

if (selected_disease != 'Selecione uma doença'):
    dt_disease = get_disease_dataset(selected_disease)
    dt_result = merge_dataset_disease(dt, dt_disease)
    moran = moran_local_bv(dt_result)
    moran_scatterplt(moran)
    moran_map(moran, dt_result)

