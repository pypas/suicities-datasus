import numpy as np
import pandas as pd
import geopandas as gpd
import glob
import scipy
from numpy import load, save
from libpysal.weights import WSP
from libpysal.weights.contiguity import Queen
from esda.moran import Moran_Local_BV, Moran

root = "../"
weights = None
mapper = None

def get_municipalities_shape():
  return gpd.read_file(root + 'Maps/BRMUE250GC_SIR.shp')

def get_muncods():
  cadmun = pd.read_csv(root + 'CSV/Cadmun/CADMUN.csv')
  cadmun = cadmun[["MUNCOD", "MUNCODDV"]]
  return cadmun

def get_avg_suicide_rates():
  suicide = pd.read_csv(root + 'CSV/Suicide/suicide_rates_08_18.csv', sep=',', index_col=0)
  suicide['AVG_SUICIDE_RATE'] = np.mean(suicide.filter(regex=("RATE_*")), axis=1)
  return suicide[['MUNCOD', 'AVG_SUICIDE_RATE']]

def get_dataset():
  gdf = get_municipalities_shape()
  codmun = get_muncods()
  suicide = get_avg_suicide_rates()

  gdf["CD_GEOCMU"] = gdf["CD_GEOCMU"].astype(int)
  gdf_city = pd.merge(gdf, codmun, left_on="CD_GEOCMU", right_on="MUNCODDV", how="left")

  result = pd.merge(gdf_city, suicide, left_on="MUNCOD", right_on="MUNCOD", how="left")
  result = result[["NM_MUNICIP", "CD_GEOCMU", "geometry", "AVG_SUICIDE_RATE"]]
  result['AVG_SUICIDE_RATE'] = result['AVG_SUICIDE_RATE'].fillna(0)
  return result

def get_disease_csv_name(disease):
  return mapper[mapper['SELECT_NAME'] == disease]['CSV'].values[0]

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

def get_disease_dataset(disease):
  print(disease)
  disease_csv_name = get_disease_csv_name(disease)
  path = 'CSV/TabNet/Internacoes_Rate/{}.csv'.format(disease_csv_name)
  disease = pd.read_csv(root + path, sep=',', index_col=0)
  disease['AVG_DISEASE_RATE'] = np.mean(disease.filter(regex=("RATE_*")), axis=1)
  disease = disease[['MUNCOD', 'AVG_DISEASE_RATE']]
  return disease

def merge_dataset_disease(dataset, disease):
  # drop column if it already exists
  dataset = dataset.drop(['AVG_DISEASE_RATE'], axis=1, errors='ignore')
  # use CD_GEOCMU with 6 digits
  dataset["CD_GEOCMU_6"] = (dataset['CD_GEOCMU'].astype(int) / 10).astype(int)
  # merge for the new disease
  result = pd.merge(dataset, disease, left_on="CD_GEOCMU_6", right_on="MUNCOD", how="left")
  result = result[["NM_MUNICIP", "CD_GEOCMU", "geometry", "AVG_SUICIDE_RATE", 'AVG_DISEASE_RATE']]
  result['AVG_SUICIDE_RATE'] = result['AVG_SUICIDE_RATE'].fillna(0)
  result['AVG_DISEASE_RATE'] = result['AVG_DISEASE_RATE'].fillna(0)
  return result

def moran_local_bv(dataset):
  x = dataset['AVG_SUICIDE_RATE'].values
  y = dataset['AVG_DISEASE_RATE'].values
  moran_bv = Moran_Local_BV(y, x, weights)
  return moran_bv

def moran_global(dataset):
  y = dataset['AVG_SUICIDE_RATE'].values
  moran = Moran(y, weights)
  return moran

def compute_weights():
  global weights
  path_to_data = "PySal/data.npy"
  weight_files = glob.glob(path_to_data)
  file_found = (len(weight_files) > 0)

  if file_found:
    data = load(path_to_data)
    spar = scipy.sparse.csc_matrix(data)
    wsp = WSP(spar)
    weights = wsp.to_W()
    print("Loaded preexisting data.npy")
  else:
    print("File data.npy not found")

  return file_found

