import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
import pickle
import altair as alt
from sklearn import metrics

# Plotting
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geoplot
import mapclassify

root = "../"

def remove_last_digit(x):
    return np.floor(x.astype(int) / 10).astype(int)

def get_test_df(satscan=False):
    if satscan:
        test_df = pd.read_csv("Models/test_data_classification_highest_rates.csv", index_col=0)
        X_test = test_df.drop(columns=["TARGET", "MUNCOD"])
        y_test = test_df["TARGET"]
        return test_df, X_test, y_test
    else:
        test_df = pd.read_csv("Models/test_data_classification_satscan.csv", index_col=0)
        X_test = test_df.drop(columns=["RISK", "MUNCOD"])
        y_test = test_df["RISK"]
        return test_df, X_test, y_test

def plot_map(y_test, y_pred, test_df, model):
    gd = gpd.read_file("EDA/BRMUE250GC_SIR.shp")

    mun_risk_ids_pred = test_df[y_pred == 1]['MUNCOD'].astype(int).tolist()
    mun_risk_ids_true = test_df[y_test == 1]['MUNCOD'].astype(int).tolist()
    mun_risk_ids_1_correct = [x for x in mun_risk_ids_pred if x in mun_risk_ids_true]

    mun_risk_ids_pred_0 = test_df[y_pred == 0]['MUNCOD'].astype(int).tolist()
    mun_risk_ids_true_0 = test_df[y_test == 0]['MUNCOD'].astype(int).tolist()
    mun_risk_ids_0_correct = [x for x in mun_risk_ids_pred_0 if x in mun_risk_ids_true_0]

    mun_risk_ids = mun_risk_ids_1_correct + mun_risk_ids_0_correct
    mun_risk_ids_wrong = [x for x in mun_risk_ids_pred if x not in mun_risk_ids_true] + [x for x in mun_risk_ids_true if x not in mun_risk_ids_pred]


    fig, ax = plt.subplots(figsize=(15,15))
    gd.plot(ax=ax, color="white", edgecolor='black')
    gd_risk = gd[remove_last_digit(gd['CD_GEOCMU']).apply(lambda x: x in mun_risk_ids)]
    plot_risk = gd_risk.plot(ax=ax, color="blue")

    gd_risk_wrong = gd[remove_last_digit(gd['CD_GEOCMU']).apply(lambda x: x in mun_risk_ids_wrong)]
    plot_risk_wrong = gd_risk_wrong.plot(ax=ax, color="red")

    blue_patch = mpatches.Patch(color='blue', label='Previsão Correta')
    red_patch = mpatches.Patch(color='red', label='Previsão Incorreta')
    plt.title("Previsões do modelo de " + model + " para o ano de 2018")
    plt.legend(handles=[red_patch,blue_patch])
    plt.axis('off')
    st.pyplot(fig)


def calculate_metrics(y_test, y_pred):
    st.write("Matriz de Confusão")
    st.write(metrics.confusion_matrix(y_test, y_pred))
    accuracy =  metrics.accuracy_score(y_test,y_pred)
    prfs = metrics.precision_recall_fscore_support(y_test,y_pred, zero_division=0)
    precision = prfs[0].mean()
    recall = prfs[1].mean()
    fscore = prfs[2].mean()
    st.write("Acurácia:", accuracy)
    st.write("Precisão:", precision)
    st.write("Revocação:", recall)
    st.write("F1-Score:", fscore)

    
def highest_rates_model(model):
    test_df, X_test, y_test = get_test_df(satscan=False)
    filename = ""
    if model != "Selecione um modelo":
        if model == "Naive Bayes":
            filename = "Models/sav/naive_bayes_highest_rates.sav"
        elif model == "Regressão Logística":
            options_scaler_highest_rates = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_highest_rates)
            if scaler == "Standard":
                filename = "Models/sav/logistic_regression_highest_rates_sc.sav"
            else:
                filename = "Models/sav/logistic_regression_highest_rates_mm.sav"
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling")
        elif model == "Random Forest":
            filename = "Models/sav/random_forest_highest_rates.sav"
        elif model == "SVC (Linear)":
            options_scaler_highest_rates = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_highest_rates)
            if scaler == "Standard":
                filename = "Models/sav/svm_linear_highest_rates_sc.sav"
            else:
                filename = "Models/sav/svm_linear_highest_rates_mm.sav"
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling")
        elif model == "SVC (RBF)":
            options_scaler_highest_rates = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_highest_rates)
            if scaler == "Standard":
                filename = "Models/sav/svm_rbf_highest_rates_sc.sav"
            else:
                filename = "Models/sav/svm_rbf_highest_rates_mm.sav"  
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling") 
        else:
            return
        
        classifier = pickle.load(open(filename, 'rb'))
        y_pred = classifier.predict(X_test) 

        calculate_metrics(y_test, y_pred)
        plot_map(y_test, y_pred, test_df, model)

def satscan_model(model):
    test_df, X_test, y_test = get_test_df(satscan=True)
    filename = ""
    if model != "Selecione um modelo":
        if model == "Naive Bayes":
            filename = "Models/sav/naive_bayes_satscan.sav"
        elif model == "Regressão Logística":
            options_scaler_satscan = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_satscan)
            if scaler == "Standard":
                filename = "Models/sav/logistic_regression_satscan_sc.sav"
            else:
                filename = "Models/sav/logistic_regression_satscan_mm.sav"
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling")
        elif model == "Random Forest":
            filename = "Models/sav/random_forest_satscan.sav"
        elif model == "SVC (Linear)":
            options_scaler_satscan = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_satscan)
            if scaler == "Standard":
                filename = "Models/sav/svm_linear_satscan_sc.sav"
            else:
                filename = "Models/sav/svm_linear_satscan_mm.sav"
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling")
        elif model == "SVC (RBF)":
            options_scaler_satscan = np.append(['MinMax'], ["Standard"])
            scaler = st.selectbox('Selecione um scaler:', options_scaler_satscan)
            if scaler == "Standard":
                filename = "Models/sav/svm_rbf_satscan_sc.sav"
            else:
                filename = "Models/sav/svm_rbf_satscan_mm.sav"  
            st.write("Modelo escolhido: ", model + " com " + scaler + " Scaling") 
        else:
            return
        
        classifier = pickle.load(open(filename, 'rb'))
        y_pred = classifier.predict(X_test) 

        calculate_metrics(y_test, y_pred)
        plot_map(y_test, y_pred, test_df, model)