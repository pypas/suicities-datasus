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
O Bivariate Moran's I é estatistica calculada para medir a **correlação espacial** entre duas grandezas.

Esse calculo é feito tomando o valor de uma variavel dependente $x$ em uma região $r_1$, e calculando uma função de agregação de
uma variavel $y$ nas regiões vizinhas da região $x$. Essa função costuma ser a **média aritmética**, e chamamos de $lag(y)$.

Apos esse calculo para cada região $r$ do mapa, calcula-se uma reta de regressão que passa pelos pontos (x_r, 
lag(y_r)) representando cada região. O coeficiente dessa reta é o **Moran's I**.
"""

"""
## **Calculo para doenças e suicidio**
"""

"""
Neste dashboard, apresentamos o mapa do Brasil subdividido em seus municipios.

A variavel dependente é uma **doença do DATASUS**, e pode ser escolhida por você!

A variavel-alvo é a **taxa de suicidios por 100.000 habitantes**.

Os municipios são coloridos de acordo com o grau de correlação espacial entre a variavel escolhida e 
a taxa de suicidios nos municipios adjacentes, para cada municipio do mapa, conforme explicado na legenda abaixo:

- HH (_High-High_): em vermelho, representa um municipio onde a taxa da doença selecionada e a taxa de suicidios na vizinhança são altos.
- LL (_Low-Low_): em azul, representa um municipio onde a taxa da doença selecionada e a taxa de suicidios na vizinhança são baixos.

Os municipios HL (_High-Low_) e LH (_Low-High_) são mostrados em cinza, pois não apresentam uma concordância 
entre o municipio e as redondezas.
"""

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

