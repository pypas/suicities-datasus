# Variáveis do DATASUS que mais impactam a saúde mental das cidades

## Objetivo

O objetivo deste projeto de TCC é descobrir quais são as variáveis do DATASUS que têm maior impacto na saúde mental das cidades, com foco principalmente na questão do suicídio nos municípios brasileiros.

## Organização do repositório

O projeto está organizado na seguinte estrutura de diretórios:

* 📁 _CSV:_ Arquivos em formato csv
  * 📁 _Cadmun_: [Fonte](ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/TABELAS/CADMUN.xls)
    * 📄 _CADMUN.csv:_ Cadastro de municípios (contém MUNCOD e Nome do município).
  * 📁 _Population_: [Fonte](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=downloads)
    * 📄 _population_08_18.csv:_ População por município (2008-2018).
  * 📁 _SatScan_
    * 📄 _case_file.csv:_ Case file para ser utilizado pelo software SatScan. Contém o número de suicídios por município e por ano.
    * 📄 _coordinates.csv:_ Coordinates file para ser utilizado pelo software SatScan. Contém as coordenadas geográficas de cada município.
    * 📄 _muncod_risk.csv:_ Municípios de alto risco, determinados pela análise feita com o software SatScan.
    * 📄 _population.csv:_ Population file para ser utilizado pelo software SatScan. Contém a população de cada município por ano.
  * 📁 _Suicide_: [Fonte](https://github.com/pypas/suicities-datasus/tree/master/TabNet)
    * 📄 _suicide_count_08_18.csv:_ Número de suicídios por município (2008-2018).
    * 📄 _suicide_rates_08_18.csv:_ Taxa de suicídios (por 100 mil habitantes) por município (2008 - 2018).
  * 📁 _TabNet:_ [Fonte](https://github.com/pypas/suicities-datasus/tree/master/TabNet)
    * 📁 _Internacoes:_ Quantidades de ocorrências de cada doença por mês por município (2008-2018).
    * 📁 _Internacoes_Anual:_ Quantidades de ocorrências de cada doença por ano por município (2008-2018).
    * 📁 _Internacoes_Rate:_ Taxa de ocorrências de cada doença por ano por município (2008-2018).
    * 📄 _Suicides:_ Taxa de suicídio por ano por município (2008-2018).
* 📁 _EDA:_ Primeira análise exploratória de dados baseada nos Dados de óbito (DO) do DATASUS.
* 📁 _Models:_ Modelos realizados com base nos rates de doenças em cada município.
  * 📁 _Classification_: Modelos de classificação de cidades por risco. Cada um dos modelos foi treinado utilizando-se 4 diferentes estratégias de preenchimentos de dados nulos.
    * 📁 _LogisticRegression:_ Modelo de classificação utilizando função logística.
    * 📁 _RandomForest:_ Modelo de regressão utilizando árvores de decisão.
    * 📁 _XGBoost:_ Modelo de ensemble de árvores de decisão.
  * 📁 _Regression:_ Modelos de predição de rates de suicídio e de diversas doenças.
    * 📄 _lasso.ipynb:_ Modelo de regressão linear com regularização L1 e seleção de variáveis.
    * 📄 _multiple\_linear\_regression.ipynb:_ Modelo de regressão linear simples.
    * 📄 _random\_forest\_regression.ipynb:_ Modelo de árvores de decisão.
    * 📄 _ridge.ipynb:_ Modelo de regressão linear com regularização L2.
    * 📁 _time\_series:_ Modelagem com Time Series dos rates nos anos de 2015-2018 (_a completar_).
  * 📁 _LinearModels:_ Primeiros modelos lineares (_deprecated_).
* 📁 _PySal_
  * 📄 _ESDA.ipynb:_ Análise exploratória espacial (ESDA) usando a biblioteca PySal para calcular Moran's BV I (autocorrelação espacial).
* 📁 _SatScan:_ Análises feitas com o software SatScan
  * 📁 _Clusters:_ Output do software SatScan (análise feita no período 2008-2018).
  * 📁 _Images:_ Imagens geradas durante a análise dos clusters.
  * 📄 _satscan.ipynb:_ Análise dos resultados obtidos pelo SatScan.
  * 📄 _satscan_data_processing.ipynb:_ Processamento de dados para serem utilizados pelo software. 
* 📁 _Spearman:_ Cálculo de correlação de Spearman entre rates de doenças e rates de suicídio, utiliza dados de Morbidade do DATASUS.
  * 📄 _spearman_analysis.ipynb:_ correlação de Spearman (2008-2018).  
* 📁 _TabNet:_ Tratamento de dados provenientes da plataforma TabNet do DATASUS
  * 📄 _suicide_format_data.ipynb:_ tratamento de dados referentes ao suicídio.
  * 📄 _diseases_format_data.ipynb:_ tratamento de dados referentes às doenças.

## Autores

Este projeto está sendo desenvolvido pelos alunos de Engenharia de Computação Quadrimestral (2020) da Escola Politécnica da USP:

* Leonardo Borges Mafra Machado - 9345213
* Marcos Paulo Pereira Moretti - 9345363
* Paula Yumi Pasqualini - 9345280

O projeto está sendo orientado pelo Professor Dr. Ricardo Luis de Azevedo da Rocha.

## Colaboradores

Este projeto está sendo realizado em parceria com o C²D e o Itaú Unibanco.
