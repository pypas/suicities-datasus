# Extração de dados do DATASUS

Os dados presentes no DATASUS utilizados no estudo foram as ocorrências de doenças e a quantidade de suicídios nos municípios brasileiros. A extração dos dados pode ser feita diretamente pelo site do DATASUS utilizando o tabulador de dados TabNet pelos links presentes abaixo:

- [Doenças](http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/nrbr.def)

- [Suicídio](http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/obt10br.def)

Devido ao grande número de doenças presentes no banco, foi feito um client para download automático de todos os dados necessários, tal client pode ser visto e executado no Jupiter Notebook `tabnet_client.ipynb`. Para formatação dos dados em taxas de ocorrência os Notebooks `internacoes_format_data.ipynb` e `suicide_format_data.ipynb` podem ser utilizados (consultar [Population](https://github.com/pypas/suicities-datasus/tree/master/CSV)).