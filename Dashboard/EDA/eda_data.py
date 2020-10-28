import pandas as pd
import matplotlib.pyplot as plt
import re,time
import streamlit as st
from collections import Counter
import seaborn as sns
import numpy as np
import altair as alt
import geopandas as gpd
import json

root = "../"

# import dask.dataframe
#suicide_df = dask.dataframe.read_csv("suicide.csv")
#suicide_df = suicide_df.drop(columns=[suicide_df.columns[0]])
suicide_df = pd.read_csv("EDA/suicide_final.csv", index_col=0)

def get_suicide_data():
    return suicide_df

# def get_cid_list():
#     cid = []
#     for index, row in suicide_df.iterrows():
#         if str(row["LINHAII"]) != "nan":
#             causa2 = str(row["LINHAII"])
#             x = causa2.split("*")
#             x.pop(0)
#             for causa in x:
#                 if re.match('A|B', causa):
#                     cid.append("A00-B99: Algumas doenças infecciosas e parasitárias")
#                 if re.match('C|D[0-3]|D4[0-8]', causa):
#                     cid.append("C00-D48: Neoplasmas (tumores)")
#                 if re.match('D[5-9]', causa):
#                     cid.append("D50-D89: Doenças do sangue e dos órgãos hematopoéticos e alguns transtornos imunitários")
#                 if re.match('E', causa):
#                     cid.append("E00-E90: Doenças endócrinas, nutricionais e metabólicas")
#                 if re.match('F', causa):
#                     cid.append("F00-F99: Transtornos mentais e comportamentais")
#                 if re.match('G', causa):
#                     cid.append("G00-G99: Doenças do sistema nervoso")
#                 if re.match('H[0-5]', causa):
#                     cid.append("H00-H59: Doenças do olho e anexos")
#                 if re.match('H[6-9]', causa):
#                     cid.append("H60-H95: Doenças do ouvido e da apófise mastoide")
#                 if re.match('I', causa):
#                     cid.append("I00-I99: Doenças do aparelho circulatório")
#                 if re.match('J', causa):
#                     cid.append("J00-J99: Doenças do aparelho respiratório")
#                 if re.match('K', causa):
#                     cid.append("K00-K93: Doenças do aparelho digestivo")
#                 if re.match('L', causa):
#                     cid.append("L00-L99: Doenças da pele e do tecido subcutâneo")
#                 if re.match('M', causa):
#                     cid.append("M00-M99: Doenças do sistema osteomuscular e do tecido conjuntivo")
#                 if re.match('N', causa):
#                     cid.append("N00-N99: Doenças do aparelho geniturinário")
#                 if re.match('O', causa):
#                     cid.append("O00-O99: Gravidez, parto e puerpério")
#                 if re.match('P', causa):
#                     cid.append("P00-P96: Algumas afecções originadas no período perinatal")
#                 if re.match('Q', causa):
#                     cid.append("Q00-Q99: Malformações congênitas, deformidades e anomalias cromossômicas")
#                 if re.match('R', causa):
#                     cid.append("R00-R99: Sintomas, sinais e achados anormais de exames clínicos e de laboratório, não classificados em outra parte")
#                 if re.match('S|T', causa):
#                     cid.append("S00-T98: Lesões, envenenamentos e algumas outras consequências de causas externas")
#                 if re.match('[V-Y]', causa):
#                     cid.append("V01-Y98: Causas externas de morbidade e de mortalidade")
#                 if re.match('Z', causa):
#                     cid.append("Z00-Z99: Fatores que influenciam o estado de saúde e o contato com os serviços de saúde")
#                 if re.match('U', causa):
#                     cid.append("U00-U99: Códigos para propósitos especiais")
#     return cid

# def plot_linha_ii():
#     cid = get_cid_list()
#     w = Counter(cid)
#     fig, ax = plt.subplots()
#     plt.xticks(rotation='vertical')
#     plt.bar(w.keys(), w.values())
#     plt.title("CID da LINHA II em casos de suicídio", loc="center", pad=10.0)
#     plt.ylabel("Número de ocorrências")
#     plt.xlabel("CID")
#     st.pyplot(fig,bbox_inches="tight")

def plot_dtobito():
    suicide_df['DTOBITO'] = pd.to_datetime(suicide_df['DTOBITO'])
    df_dtobito = suicide_df[["DTOBITO"]]
    df_dtobito["DTOBITO"] = df_dtobito["DTOBITO"].dt.tz_localize('America/Argentina/Catamarca')

    scales = alt.selection_interval(bind='scales')
    graph = alt.Chart(df_dtobito, title="Quantidade de suicídios por mês (2008-2018)").mark_line(point=True).encode(
        x=alt.X('utcyearmonth(DTOBITO)', title='Mês/Ano'),
        y=alt.Y('count()', title='Quantidade'),
        tooltip=[alt.Tooltip('utcyearmonth(DTOBITO)', title='Mês/Ano'), alt.Tooltip('count()', title='Quantidade')]
    ).add_selection(scales).interactive()

    st.altair_chart((graph).configure_view(strokeOpacity=0).configure_title(fontSize=12).properties(width=700, height=410))

def plot_column(column):
    if column == "Idade":
        df_idade = suicide_df[suicide_df["IDADE"] > 0][["IDADE"]]

        graph = alt.Chart(df_idade, title="Quantidade de suicídios por idade (2008-2018)").mark_bar().encode(
             alt.X("IDADE", title="Idade"),
             y=alt.Y('count()', title='Quantidade'),
             tooltip=[alt.Tooltip('IDADE', title='Idade'), alt.Tooltip('count()', title='Quantidade')],
             color=alt.condition(
                alt.datum.IDADE == int(df_idade["IDADE"].mean()),
                alt.value('orange'),
                alt.value('steelblue')
            )
        )

        text = graph.mark_text(
            align='left',
            baseline='middle',
            dx=5
        ).encode(
            text=alt.value("Média"),
                opacity= alt.condition(
            alt.datum.IDADE == int(df_idade["IDADE"].mean()), 
            alt.value(1.0),
            alt.value(0.0))
        )

        st.altair_chart((graph + text).configure_view(strokeOpacity=0).configure_title(fontSize=12).properties(width=700, height=410))
    elif column == "Sexo":
        df_sexo = suicide_df[["SEXO", "YEAR"]]
        scales = alt.selection_interval(bind='scales')
        graph = alt.Chart(df_sexo, title="Quantidade de suicídios por sexo (2008 - 2018)").mark_line(point=True).encode(
            x=alt.X("YEAR:N", title="Ano"),
            y=alt.Y('count()', title='Quantidade'),
            color='SEXO',
            strokeDash='SEXO',
            tooltip=[alt.Tooltip('SEXO', title='Sexo'), alt.Tooltip('count()', title='Quantidade')],
        ).add_selection(scales).interactive()
        
        # base = alt.Chart(df_sexo, title="Quantidade de suicídios por sexo (2008 - 2018)").encode(alt.X('YEAR:N', axis=alt.Axis(title='Ano')))

        # graph_m = base.mark_line().encode( alt.Y('count()', axis=alt.Axis(title='Quantidade de Suicídios (M)'))).transform_filter(
        #     (alt.datum.SEXO == "M")
        # )
        # graph_f = base.mark_line(color="#ffd100").encode( alt.Y('count()', axis=alt.Axis(title='Quantidade de Suicídios (F)'))).transform_filter(
        #     (alt.datum.SEXO == "F")
        # )

        # actual_date_graph = (graph_m + graph_f).resolve_scale(y='independent')

        st.altair_chart((graph).configure_view(strokeOpacity=0).configure_title(fontSize=12).properties(width=700, height=410))
    elif column == "Estado Civil":
        options = np.append(['Todos'], [x for x in range(2008,2019)] + ["Todos"])
        ano = st.selectbox('Selecione um ano:', options)
        if ano == "Todos":
            df_estciv = suicide_df[["ESTCIV"]]
            ano = "2008-2018"
        else:
            df_estciv = suicide_df[suicide_df["YEAR"] == int(ano)][["ESTCIV"]]
        df_estciv = df_estciv[df_estciv["ESTCIV"].isna() == 0]
        scales = alt.selection_interval(bind='scales')

        graph = alt.Chart(df_estciv, title="Quantidade de suicídios por estado civil (" + ano + ')').mark_bar(color="#00336E").encode(
         alt.X("ESTCIV", title="Estado Civil"),
             y=alt.Y('count()', title='Quantidade'),
             color=alt.Color('ESTCIV:N', legend=None),
             tooltip=[alt.Tooltip('ESTCIV', title='Estado Civil'), alt.Tooltip('count()', title='Quantidade')]
         ).add_selection(scales).interactive()

        st.altair_chart((graph).configure_view(strokeOpacity=0).properties(width=700, height=410))
    elif column == "Raça/Cor":
        options = np.append(['Todos'], [x for x in range(2008,2019)] + ["Todos"])
        ano = st.selectbox('Selecione um ano:', options)
        if ano == "Todos":
            df_racacor = suicide_df[["RACACOR"]]
            ano = "2008-2018"
        else:
            df_racacor = suicide_df[suicide_df["YEAR"] == int(ano)][["RACACOR"]]
        df_racacor = df_racacor[df_racacor["RACACOR"].isna() == 0]
        scales = alt.selection_interval(bind='scales')

        graph = alt.Chart(df_racacor, title="Quantidade de suicídios por raça/cor (" + ano + ')').mark_bar(color="#00336E").encode(
         alt.X("RACACOR", title="Raça/Cor"),
             y=alt.Y('count()', title='Quantidade'),
             color=alt.Color('RACACOR:N', legend=None),
             tooltip=[alt.Tooltip('RACACOR', title='Raça/Cor'), alt.Tooltip('count()', title='Quantidade')]
         ).add_selection(scales).interactive()

        st.altair_chart((graph).configure_view(strokeOpacity=0).properties(width=700, height=410))
    elif column == "Escolaridade":
        options = np.append(['Todos'], [x for x in range(2008,2019)] + ["Todos"])
        ano = st.selectbox('Selecione um ano:', options)
        if ano == "Todos":
            df_esc = suicide_df[["ESC"]]
            ano = "2008-2018"
        else:
            df_esc = suicide_df[suicide_df["YEAR"] == int(ano)][["ESC"]]
        df_esc = df_esc[df_esc["ESC"].isna() == 0]
        scales = alt.selection_interval(bind='scales')

        graph = alt.Chart(df_esc, title="Quantidade de suicídios por escolaridade (" + ano + ')').mark_bar(color="#00336E").encode(
         alt.X("ESC", title="Escolaridade"),
             y=alt.Y('count()', title='Quantidade'),
             color=alt.Color('ESC:N', legend=None),
             tooltip=[alt.Tooltip('ESC', title='Escolaridade'), alt.Tooltip('count()', title='Quantidade')]
         ).add_selection(scales).interactive()

        st.altair_chart((graph).configure_view(strokeOpacity=0).properties(width=700, height=410))
    elif column == "Ocupação":
        counter = Counter(list(suicide_df["OCUP"]))
        jobs = []
        count = []
        for i in counter.most_common(20):
            jobs.append(i[0])
            count.append(i[1])

        source = pd.DataFrame({'JOBS': jobs,
                           'COUNT': count})
        graph = alt.Chart(source, title="Quantidade de suicídios por ocupação (2008-2018)").mark_bar().encode(
            x=alt.X('COUNT', title="Quantidade"),
            color=alt.Color('JOBS:N', legend=None),
            y=alt.Y('JOBS', title="Ocupação", sort='-x'),
            tooltip=[alt.Tooltip('JOBS', title='Ocupação'), alt.Tooltip('COUNT', title='Quantidade')]
        )
        st.altair_chart((graph).properties(width=700, height=410))

def plot_codmunres():
    gdf = gpd.read_file(root + 'Maps/BRMUE250GC_SIR.shp')
    cadmun = pd.read_csv(root + 'CSV/Cadmun/CADMUN.csv')
    cadmun = cadmun[["MUNCOD", "MUNCODDV"]]
  
    gdf["CD_GEOCMU"] = gdf["CD_GEOCMU"].astype(int)
    gdf_city = pd.merge(gdf, cadmun, left_on="CD_GEOCMU", right_on="MUNCODDV", how="left")

    counter = Counter(list(suicide_df["CODMUNRES"]))
    codmunres_df = pd.DataFrame({'MUNCOD': list(dict(counter).keys()),
                           'COUNT': list(dict(counter).values())})
    result = pd.merge(gdf_city, codmunres_df, left_on="MUNCOD", right_on="MUNCOD", how="left")
    result = result[["NM_MUNICIP", "CD_GEOCMU", "geometry", "COUNT"]]
    fig, ax = plt.subplots()
    result.plot(ax=ax, column='COUNT', cmap =    
                                'YlGnBu', figsize=(15,9),   
                                 scheme='quantiles', k=4, legend=True)
    plt.title("Quantidade de suicídios por município de residência")
    st.pyplot(fig)
