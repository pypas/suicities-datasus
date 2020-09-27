import streamlit as st
import numpy as np
import pandas as pd
import time
from splot.esda import moran_scatterplot, lisa_cluster
from bivariate_data import compute_weights, get_dataset, get_disease_dataset, merge_dataset_disease, moran_local_bv, moran_global

def moran_scatterplt(moran, bivariate=False, disease=''):
    if bivariate:
        fig, ax = moran_scatterplot(moran, p=0.05)
        ax.set_ylabel('Spatial lag of ' + disease)
    else:
        fig, ax = moran_scatterplot(moran, aspect_equal=True)
        ax.set_ylabel('Spatial lag of Suicides')

    ax.set_xlabel('Suicides')
    st.pyplot(fig)

def moran_map(moran, dataset):
    fig = lisa_cluster(moran, dataset, p=0.05, figsize=(9,9))
    st.pyplot(fig)

compute_weights()
dt = get_dataset()

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
## **Cálculo para a variável-alvo taxa de suicídios**
"""

"""
Primeiramente, vamos analisar somente a variável-alvo (taxa de suicídios) contra o $lag$ da variável-alvo.

Ou seja, estamos tomando $x$ como sendo a variável-alvo taxa de suicídios em uma região $r$ e $y$ como sendo a mesma variável, 
mas na vizinhança da cidade $r$ considerada.

Com essa análise, conseguimos ter uma noção da importância da relação espacial da variável-alvo, por meio do valor do Moran's I.
"""

moran = moran_global(dt)
moran_scatterplt(moran, bivariate=False)


"""
## **Cálculo para doenças e suicídio**
"""

"""
Em seguida, apresentamos o mapa do Brasil subdividido em seus municípios.

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

selected_disease = st.selectbox(
    'Selecione uma doença:',
    ['Selecione uma doença', 'Artrose'])

if (selected_disease != 'Selecione uma doença'):
    dt_disease = get_disease_dataset(selected_disease)
    dt_result = merge_dataset_disease(dt, dt_disease)
    moran_bv = moran_local_bv(dt_result)
    moran_scatterplt(moran_bv, bivariate=True, disease=selected_disease)
    moran_map(moran_bv, dt_result)

