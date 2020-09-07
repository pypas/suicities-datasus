import streamlit as st
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

st.write("""
# Correlação de Spearman
Para determinar a relação das diversas doenças com o suicídio nas cidades, foi realizada uma correlação de Spearman entre as taxas de internações correspondentes a cada uma delas e a taxa de suicídio por município, no período de 2008 a 2018.
""")

# Leitura dos arquivos
root = "../"
path = root + "CSV/TabNet/Internacoes_Rate/"
all_files = glob.glob(path + "*.csv")
suicide_df = pd.read_csv(root + 'CSV/Suicide/suicide_rates_08_18.csv', sep=',', index_col=0)



st.subheader('Taxa de suicidios por município')
st.write(suicide_df)

disease = ""
years = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
suicide_df["SUICIDE"] = suicide_df.drop(columns="MUNCOD").sum(axis=1)/(len(suicide_df.columns) - 1)
suicide_df = suicide_df[["MUNCOD", "SUICIDE"]]

corrs_list = []
p_value_list = []
size_list = []
diseases_list = []

for file in all_files:
    file_name = file.split("\\")[1]
    disease = file_name.split(".csv")[0]
    disease_df = pd.read_csv(path + disease + '.csv', sep=',', index_col=0) 
    disease_df["Total"] = disease_df.drop(columns="MUNCOD").sum(axis=1)/(len(disease_df.columns) - 1)
    disease_df = disease_df[["MUNCOD", "Total"]]
    disease_df = disease_df[(disease_df["Total"] != 0)] # Excluded rows with 0 suicides
    if disease_df.shape[0] > 2500:
        final_df = pd.merge(disease_df, suicide_df, on="MUNCOD")		 
        corr, p_value = spearmanr(final_df["Total"],final_df["SUICIDE"])
        if p_value < 0.05:
        	size_list.append(final_df.shape[0])
	        corrs_list.append(corr)
	        diseases_list.append(disease)
	        p_value_list.append(p_value)
        
corrs_data = {'Doença': diseases_list, 'Correlação com suicidio': corrs_list, 'P value': p_value_list, "Municípios incluídos": size_list}
corrs_df = pd.DataFrame(data=corrs_data)

st.subheader('Top 50 doenças com correlação positiva')
st.write(corrs_df.sort_values(by=['Correlação com suicidio'], ascending=False).reset_index(drop=True).head(50))

st.subheader('Doenças com correlação negativa')
st.write(corrs_df[corrs_df["Correlação com suicidio"] < 0].sort_values(by=['Correlação com suicidio'], ascending=True).reset_index(drop=True))

# Definicao dos parâmetros
st.sidebar.header('Parâmetros')
doenca = st.sidebar.selectbox(
    "Doença a ser plotada",
    diseases_list
    )

st.subheader('Doença escolhida')
st.write(doenca)

disease_df = pd.read_csv(path + doenca + '.csv', sep=',', index_col=0) 
disease_df["Total"] = disease_df.drop(columns="MUNCOD").sum(axis=1)/(len(disease_df.columns) - 1)
disease_df = disease_df[["MUNCOD", "Total"]]
disease_df = disease_df[(disease_df["Total"] != 0)] # Excluded rows with 0 suicides
final_df = pd.merge(disease_df, suicide_df, on="MUNCOD")
plt.scatter(final_df["Total"], final_df["SUICIDE"], s=5)
plt.ylabel("Taxa de suicidios")
plt.xlabel("Taxa de Internações (" + doenca + ")")
st.pyplot(dpi=100)