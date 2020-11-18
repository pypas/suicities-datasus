import streamlit as st
from Homepage.homepage import present_homepage
import EDA.eda_view as eda_vw
import PySal.bivariate_view as moran_vw
import Spearman.spearman_view as spearman_vw
import SatScan.satscan_view as satscan_vw
import Models.classification_model_view as classification_vw

st.sidebar.title("Dashboard")
dashboard = st.sidebar.selectbox("Escolha o dashboard que deseja ver:", ["Homepage", "Análise Exploratória de Dados", 
	"Análise de Correlação de Spearman", "Análise de Autocorrelação Espacial", "Determinação de Clusters de Suicídio", "Modelos Preditivos"])
if dashboard == "Homepage":
    present_homepage()
elif dashboard == "Análise Exploratória de Dados":
    eda_vw.present_eda()
elif dashboard == "Análise de Autocorrelação Espacial":
    moran_vw.present_moran()
elif dashboard == "Determinação de Clusters de Suicídio":
	satscan_vw.present_satscan()
elif dashboard == "Análise de Correlação de Spearman":
    spearman_vw.present_spearman()
else:
	classification_vw.present_classification_model()
