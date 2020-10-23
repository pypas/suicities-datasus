import streamlit as st
from Homepage.homepage import present_homepage

st.sidebar.title("Dashboard")
dashboard = st.sidebar.selectbox("Escolha o dashboard que deseja ver:", ["Homepage", "EDA", "Bivariate Moran's I", "Spearman"])
if dashboard == "Homepage":
    present_homepage()
elif dashboard == "EDA":
    st.sidebar.success("EDA")
elif dashboard == "Bivariate Moran's I":
    st.sidebar.success("Bivariate Moran's I")
else:
    st.sidebar.success("Spearman")
