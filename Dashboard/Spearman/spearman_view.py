import streamlit as st
import numpy as np
from . import spearman_data as dt

def present_spearman():
    st.markdown(
        """
        # Análise de correlação de Spearman

        Para determinar a relação das diversas doenças com o suicídio nas cidades, foi realizada uma correlação de Spearman 
        entre as taxas de internações correspondentes a cada uma delas e a taxa de suicídio por município, no período de 2008 a 2018.

        """
    )

    st.markdown(
        """
        ## Coeficiente de correlação de Spearman

        O coeficiente de **correlação de Spearman** é uma medida da intensidade e direção da associação monotônica entre duas variáveis.
        Em outras palavras, ele avalia o quão bem a relação entre duas variáveis pode ser descrita por meio de uma relação monotônica.

        O cálculo do coeficiente é feito através de uma correlação de Pearson entre os **rankings** das variáveis. O valor obtido é $r_s$, que é 
        tal que $-1 \leq r_s \leq 1$:
        - $r_s = 1$ indica uma associação perfeita e positiva entre as váriáveis
        - $r_s = 0$ indica que não há nenhuma associação entre as variáveis
        - $r_s = -1$ indica uma associação perfeita e negativa entre as variávels

        """
    )

    st.markdown(
        """
        ## Tabela de correlações com suicídio

        A tabela abaixo contém os coeficientes de correlações de Spearman (bem como seus respectivos _p-values_) entre a média da taxa de internações referentes a diferentes doenças do DATASUS e a média da taxa de suicídios, no período de 2008-2018. 

        A coluna "Qtd Municípios" indica a quantidade de municípios com dados não nulos presentes no conjunto de dados de cada doença. 
        Foram excluídas as doenças cuja quantidade de municípios é inferior à metade do número total de municípios no Brasil, ou seja, $< 2785$.

        """
    )

    st.write(dt.get_top_correlations())

    st.markdown(
        """
        ## Gráfico de Doenças vs Suicídio

        """
    )

    disease_names = dt.get_diseases_select_names()
    if len(disease_names) > 0:
        options = np.append(['Selecione uma doença'], disease_names)
        selected_disease = st.selectbox('Selecione uma doença:', options)

        st.markdown(
            '<p>Para mais informações sobre uma doença, acesse o <a href="http://tabnet.datasus.gov.br/cgi/sih/mxcid10lm.htm", target="_blank">DATASUS</a>.</p>', unsafe_allow_html=True
        )

        if (selected_disease != 'Selecione uma doença'):
            dt.plot_disease_vs_suicide(selected_disease)
    else:
        st.markdown(
            """
            ### **_Erro ao carregar nomes das doenças._**
            """
        )