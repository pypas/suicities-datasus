import streamlit as st
from Homepage.homepage import present_homepage
import EDA.eda_view as eda_vw
import PySal.bivariate_view as moran_vw
import Spearman.spearman_view as spearman_vw
import SatScan.satscan_view as satscan_vw

st.sidebar.title("Dashboard")
dashboard = st.sidebar.selectbox("Escolha o dashboard que deseja ver:", ["Homepage", "EDA", "Bivariate Moran's I", "Spearman", "SatScan"])
if dashboard == "Homepage":
    present_homepage()
elif dashboard == "EDA":
    eda_vw.present_eda()
elif dashboard == "Bivariate Moran's I":
    moran_vw.present_moran()
elif dashboard == "SatScan":
	satscan_vw.present_satscan()
else:
    spearman_vw.present_spearman()
