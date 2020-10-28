import streamlit as st
from Homepage.homepage import present_homepage
import EDA.eda_view as eda_vw
import PySal.bivariate_view as moran

st.sidebar.title("Dashboard")
dashboard = st.sidebar.selectbox("Escolha o dashboard que deseja ver:", ["Homepage", "EDA", "Bivariate Moran's I", "Spearman"])
if dashboard == "Homepage":
    present_homepage()
elif dashboard == "EDA":
    eda_vw.present_eda()
elif dashboard == "Bivariate Moran's I":
    moran.present_moran()
else:
    st.sidebar.success("Spearman")
