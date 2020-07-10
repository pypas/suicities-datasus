# Variáveis do DATASUS que mais impactam a saúde mental das cidades

## Objetivo

O objetivo deste projeto de TCC é descobrir quais são as variáveis do DATASUS que têm maior impacto na saúde mental das cidades, com foco principalmente na questão do suicídio nos municípios brasileiros.

## Organização do repositório

O projeto está organizado na seguinte estrutura de diretórios:

* 📁 _CIHA:_ Análises com dados de Internação Hospitalar (CIHA) do DATASUS.
* 📁 _EDA:_ Primeira análise exploratória de dados baseada nos Dados de óbito (DO) do DATASUS.
* 📁 _LinearModels:_ Primeiros modelos lineares (_deprecated_).
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
* 📁 _PySal_
  * 📁 _municipios:_ .shp dos municípios brasileiros.
  * 📄 _ESDA.ipynb:_ Análise exploratória espacial (ESDA) usando a biblioteca PySal para calcular Moran's BV I (autocorrelação espacial).
* 📁 _Spearman:_ Cálculo de correlação de Spearman entre rates de doenças e rates de suicídio, utiliza dados de Morbidade do DATASUS.
  * 📄 _spearman.ipynb:_ correlação de Spearman em 2017.
  * 📄 _spearman\_2015\_2017.ipynb:_ correlação de Spearman em 2015-2017.
  * 📁 _CSV:_ 
    * 📁 _Quantity:_ Quantidades de ocorrências de cada doença por município em 2017.
    * 📁 _Rates:_ Rates de cada doença por município em 2017.
    * 📄 _transform\_tabnet.ipynb:_ Calcula rates de doenças com base nas quantidades e população de cada município.
* 📁 _Suicide:_ Apresenta quantidades e rates de suicídio por cidade, de 2015 a 2018 separadamente, e agregados de 2015-2017.
* 📁 _TabNet:_ Apresenta dados compilados provenientes da plataforma TabNet do DATASUS
  * 📁 _Quantity:_ Quantidades de ocorrências de cada doença por município em 2015 a 2018, separadamente.
  * 📁 _Rates:_ Rates de cada doença por município em 2015 a 2018, separadamente.
  * 📁 _PNG:_ Plots do mapa do Brasil para cada doença.
  * 📄 _plot\_disease\_distribution.ipynb:_ Faz plot do mapa do Brasil hachurado de acordo com o rate municipal de uma doença.
* 📁 _util:_ Arquivos adicionais utilizados.
  * 📁 _Population:_ População por município em 2015 a 2018 e agregados.
  * 📄 _CADMUN.csv:_ Cadastro de municípios (contém MUNCOD e Nome do município).
  * 📄 _CID10.csv:_ Classificação internacional de doenças.
  * 📄 _plot\_disease\_distribution.ipynb:_ Faz plot do mapa do Brasil hachurado de acordo com o rate municipal de uma doença.

## Autores

Este projeto está sendo desenvolvido pelos alunos de Engenharia de Computação Quadrimestral (2020) da Escola Politécnica da USP:

* Leonardo Borges Mafra Machado - 9345213
* Marcos Paulo Pereira Moretti - 9345363
* Paula Yumi Pasqualini - 9345280

O projeto está sendo orientado pelo Professor Dr. Ricardo Luis de Azevedo da Rocha.

## Colaboradores

Este projeto está sendo realizado em parceria com o C²D e o Itaú Unibanco.
