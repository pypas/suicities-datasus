import re
import pandas as pd
df = pd.read_csv('DOBR2017.csv', sep=',')
df = df[["CAUSABAS", "CODMUNOCOR"]]
df_causabas = df[df['CAUSABAS'].notnull() & df["CAUSABAS"].str.contains(pat = '(X[6-7])|(X8[0-4])', regex = True)]
df_causabas = df_causabas[["CODMUNOCOR"]]
df_new = df_causabas.groupby(['CODMUNOCOR']).size().to_frame('SUICIDES')

mun = pd.read_csv('CADMUN.csv', sep=',')
mun = mun[["MUNCOD", "MUNNOME", "LATITUDE", "LONGITUDE"]]

result = pd.merge(df_new, mun, left_on="CODMUNOCOR", right_on="MUNCOD", how="inner")

result.to_csv(r'suicide_by_city.csv')

