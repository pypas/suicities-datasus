import streamlit as st
import streamlit.components.v1 as components
import numpy as np

def present_satscan():
	st.markdown(
		"""
		# SatScan
		"""
		"""
		O *SatScan* é um software gratuito amplamente utilizado para identificar *clusters* espaciais de 
		doenças e verificar se eles são estatisticamente significativos.

		Neste estudo, foi utilizada a ferramenta de varredura espacial, que posiciona no mapa janelas circulares 
		de diferentes raios, sendo cada um dos círculos gerados um potencial candidato a *cluster*. 
		Os *clusters* encontrados são avaliados e é gerado um relatório contendo os resultados da análise, 
		que pode ser visualizado abaixo. 
		"""
	)

	analysis = st.radio("Qual tipo de análise?",('cluster', 'clustermap'))

	options = np.append(['Selecione um ano'], [str(x) for x in range(2008,2019)])
	year = st.selectbox('Selecione um ano:', options)
	if year != "Selecione um ano":
		HtmlFile = open("SatScan/output_" + year + "." + analysis + ".html", 'r')
		source_code = HtmlFile.read() 
		components.html(source_code, height = 1200, scrolling = True)
	