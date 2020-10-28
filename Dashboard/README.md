## Instruções

Para rodar este Dashboard, execute:

`streamlit run startup.py`

Bibliotecas:

- libpysal=4.2.2
- esda=2.2.1
- streamlit=0.67.1

## Pré-requisitos

A seguir, estão os arquivos necessarios para rodar cada Dashboard:

### EDA

- Ter o arquivo `EDA/suicide_final.csv`

### Bivariate Moran's I

- Ter os arquivos `Maps/BRMUE250GC_SIR.*`
- Ter gerado o arquivo `Dashboard/PySal/data.npy` a partir do arquivo `PySal/ESDA_monthly_rates.ipynb`
- Ter gerado o arquivo `Dashboard/diseases_select_list.csv` a partir do arquivo `Dashboard/diseases_list_generator.ipynb`

### Spearman

- Ter gerado o arquivo `Dashboard/Spearman/correlation.csv` a partir do arquivo `Spearman/spearman.ipynb`
- Ter gerado o arquivo `Dashboard/diseases_select_list.csv` a partir do arquivo `Dashboard/diseases_list_generator.ipynb`