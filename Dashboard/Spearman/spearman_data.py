import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import streamlit as st

root = "../"
path = root + "CSV/TabNet/Internacoes_Rate/"
corrs_df = pd.read_csv("Spearman/correlation.csv",index_col=0)

def get_top_correlations(ascending = False):
    corrs_df["Doenças"] = corrs_df["Doenças"].str.title().str.replace('_', ' ')
    return corrs_df.sort_values(by=['Correlação com suicidio'], ascending=ascending).reset_index(drop=True)

def plot_disease_vs_suicide(disease):
    csv_disease = mapper[mapper['SELECT_NAME'] == disease]['CSV'].values[0]
    suicide_df = pd.read_csv(root + 'CSV/Suicide/suicide_rates_08_18.csv', sep=',', index_col=0)
    suicide_df["SUICIDE"] = suicide_df.drop(columns="MUNCOD").sum(axis=1)/(len(suicide_df.columns) - 1)
    disease_df = pd.read_csv(path + csv_disease + '.csv', sep=',', index_col=0) 
    disease_df["Total"] = disease_df.drop(columns="MUNCOD").sum(axis=1)/(len(disease_df.columns) - 1)
    disease_df = disease_df[["MUNCOD", "Total"]]
    disease_df = disease_df[(disease_df["Total"] != 0)] # Exclude rows with 0 suicides
    final_df = pd.merge(disease_df, suicide_df, on="MUNCOD")
    fig, ax = plt.subplots()
    ax.scatter(final_df["Total"], final_df["SUICIDE"], s=5)
    plt.title("Suicídios vs " + disease + " (2008-2018)")
    plt.ylabel("Taxa de suicídios")
    plt.xlabel("Taxa de Internações (" + disease + ")")
    st.pyplot(fig, dpi=100)

def get_diseases_select_names():
    global mapper
    diseases_files = glob.glob("diseases_select_list.csv")
    file_found = (len(diseases_files) > 0)

    if file_found:
        mapper = pd.read_csv('diseases_select_list.csv', index_col=0)
        print("Loaded preexisting diseases_select_list.csv")
        return np.array(mapper['SELECT_NAME'])
    else:
        print("File diseases_select_list.csv not found")
        return []