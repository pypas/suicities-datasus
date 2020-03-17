import glob
import os
from simpledbf import Dbf5
import urllib.request
import pandas as pd

def download_dbc(url, file):
    # Retrieves dbc file from URL
    urllib.request.urlretrieve(url, file + '.dbc')

def dbc_to_dbf(file):
    # Converts dbc to dbf
    os.system('dbf2dbc ' + file + '.dbc')

def dbf_to_csv(file):
    dbf = Dbf5(file + '.dbf', codec='utf-8')
    # Converts dbf to csv
    dbf.to_csv(file + '.csv')

def fetch_files_csv(files):
    for file in files:
        url = 'ftp://ftp.datasus.gov.br/dissemin/publicos/CIHA/201101_/Dados/' + file + '.dbc'
        download_dbc(url, file)

#     # Change directory
#     os.chdir('fetch_data')

    for file in files:
        dbc_to_dbf(file)
        os.system('del /f ' + file + '.dbc')

    for file in files:
        dbf_to_csv(file)
        os.system('del /f ' + file + '.dbf')


#estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
# #           "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
estado = "SP"
ano = "17"
files = []
for mes in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    files.append('CIHA' + estado + ano + mes)

# Fetch files
os.chdir('fetch_data')
fetch_files_csv(files)

# # Change directory
# os.chdir('fetch_data')
#
# Merge csv files
all_files = glob.glob("*.csv")
df = pd.concat((pd.read_csv(f, header = 0, low_memory=False) for f in all_files))
df.to_csv("CIHA" + estado + ano + ".csv")

# Delete month csv files
for file in files:
    os.system('del /f ' + file + '.csv')


