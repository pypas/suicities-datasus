#https://towardsdatascience.com/how-to-build-a-simple-machine-learning-web-app-in-python-68a45a0e0291
import streamlit as st
import pandas as pd
import glob
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from datetime import datetime

# Import Statsmodels
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
#_max_width_()

st.write("""
# Séries Temporais
""")

st.sidebar.header('User Input Parameters')

chosen = ["TRANSTORNOS_DE_HUMOR_[AFETIVOS]", "TRANST_MENTAIS_E_COMPORTAMENTAIS_DEV_USO_DE_ÁLCOOL", "NEOPLASIA_MALIGNA_DO_CÓLON", "NEOPL_MALIG_JUNÇÃO_RETOSSIGM_RETO_ÂNUS_CANAL_ANAL", "BRONQUITE_ENFISEMA_E_OUTR_DOENÇ_PULM_OBSTR_CRÔNIC"]
doencas = [" ".join(x.split("_")) for x in chosen]

municipio = st.sidebar.selectbox(
    "Qual o Município desejado?",
    ("355030 São Paulo", "350950 Campinas", "292740 Salvador")
    )

doenca = st.sidebar.selectbox(
    "Doença a ser plotada",
    doencas
    )

st.subheader('Município escolhido')
st.write(municipio)

root = "../"
path = root + 'CSV/TabNet/Internacoes/'
all_files = glob.glob(path + "*")
df_diseases = pd.DataFrame()
list_of_diseases = []
for disease in chosen:
    list_of_diseases.append(disease)
    df_disease = pd.read_csv(path + disease + ".csv", sep=";")
    df_disease = df_disease[df_disease["Município"] == municipio]
    if not df_disease.empty:
        df_disease= df_disease.filter(regex='2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018', axis=1)
        df_disease = df_disease.transpose()
        df_disease.columns = [disease]
        df_disease = df_disease.replace("-",0)
        df_disease = df_disease.astype(int)
        df_diseases[disease] = df_disease[disease]
df_diseases = df_diseases.fillna(0)

month_dic = {
    "Jan": "January",
    "Fev": "February",
    "Mar": "March",
    "Abr": "April",
    "Mai": "May",
    "Jun": "June",
    "Jul": "July",
    "Ago": "August",
    "Set": "September",
    "Out": "October",
    "Nov": "November",
    "Dez": "December"
}
indexes = []
for i,e in enumerate(df_diseases.index): 
    ano = e.split("/")[0]
    mes = e.split("/")[1]
    month = month_dic[mes]
    datetime_object = datetime.strptime(month, "%B")
    indexes.append(str(datetime_object.month) + "/" + str(ano))
df_diseases.index = indexes

path = root + 'CSV/TabNet/Suicides/'
all_files = glob.glob(path + "*")
df_suicides = pd.DataFrame()
list_of_years = []
for file in all_files:
    file_name = file.split("\\")[1]
    year = file_name.split("_")[1].split(".")[0]
    list_of_years.append(year)
    df_year = pd.read_csv(path + file_name, sep=";")
    df_year = df_year.replace("-",0)
    df_year = df_year[df_year["Município"] == municipio]
    df_year = df_year.drop(columns=["Município", "Total"])
    if not df_year.empty:
        df_year = df_year.transpose()
        df_year.columns = ["SUICIDE"]
        df_year = df_year.astype(int)
        df_year.index = df_year.index + "/" + year
        df_suicides = pd.concat([df_suicides, df_year])


from datetime import datetime
month_dic = {
    "Janeiro": "January",
    "Fevereiro": "February",
    "Março": "March",
    "Abril": "April",
    "Maio": "May",
    "Junho": "June",
    "Julho": "July",
    "Agosto": "August",
    "Setembro": "September",
    "Outubro": "October",
    "Novembro": "November",
    "Dezembro": "December"
}
indexes = []
for i,e in enumerate(df_suicides.index): 
    mes = e.split("/")[0]
    ano = e.split("/")[1]
    month = month_dic[mes]
    datetime_object = datetime.strptime(month, "%B")
    indexes.append(str(datetime_object.month) + "/" + str(ano))
df_suicides.index = indexes

df = df_diseases.copy()
df["SUICIDE"] = df_suicides["SUICIDE"]
st.subheader('Tabela')
st.write(df)

df.columns = [" ".join(x.split("_")) for x in df.columns]

df[doenca].plot()
plt.title(doenca)
plt.xlabel("Mês/Ano")
plt.ylabel("Quantidade")
st.pyplot(dpi=100)

st.subheader('Shape')
st.write("Número de linhas: " + str(df.shape[0]))
st.write("Número de colunas: " + str(df.shape[1]))

df["SUICIDE"].plot()
plt.title("Suicídios no município de " + municipio.split(" ",1)[1])
plt.xlabel("Mês/Ano")
plt.ylabel("Quantidade")
st.pyplot(dpi=100)

## Causalidade
from statsmodels.tsa.stattools import grangercausalitytests
maxlag=12
test = 'ssr_chi2test'
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False): 
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    return df

st.subheader('Granger Causation Matrix')
st.write(grangers_causation_matrix(df, variables = df.columns))

## 5 - Split into train and test
nobs = 4
df_train, df_test = df[0:-nobs], df[-nobs:]

## 6 - Stationarity
df_differenced = df_train.diff().dropna()
model = VAR(df_differenced)
model_fitted = model.fit(2)
model_fitted.summary()

lag_order = model_fitted.k_ar
forecast_input = df_differenced.values[-lag_order:]

fc = model_fitted.forecast(y=forecast_input, steps=nobs)
df_forecast = pd.DataFrame(fc, index=df.index[-nobs:], columns=df.columns + '_1d')

def invert_transformation(df_train, df_forecast, second_diff=False):
    """Revert back the differencing to get the forecast to original scale."""
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        # Roll back 2nd Diff
        if second_diff:
            df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
        # Roll back 1st Diff
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()
    return df_fc

df_results = invert_transformation(df_train, df_forecast, second_diff=False)
forecast_array = []
chosen.append("SUICIDE")
for i in chosen:
    forecast_array.append(i + "_forecast")

st.subheader('Predições x Realidade')
df_results['SUICIDE_forecast'].plot(legend=True)
df_test["SUICIDE"][-nobs:].plot(legend=True);
plt.title("Previsões para o município de " + municipio.split(" ",1)[1] + " (09/2018 - 12/2018)")
plt.xlabel("Mês/Ano")
plt.ylabel("Quantidade")
st.pyplot(dpi=100)

st.subheader('RMSE')
rmse = np.mean((df_results['SUICIDE_forecast'].values - df_test["SUICIDE"])**2)**.5  # RMSE
st.write(rmse)

st.subheader('Predições x Realidade')
df_results[doenca + '_forecast'].plot(legend=True)
df_test[doenca][-nobs:].plot(legend=True);
plt.title("Previsões para o município de " + municipio.split(" ",1)[1] + " (09/2018 - 12/2018)")
plt.xlabel("Mês/Ano")
plt.ylabel("Quantidade")
st.pyplot(dpi=100)