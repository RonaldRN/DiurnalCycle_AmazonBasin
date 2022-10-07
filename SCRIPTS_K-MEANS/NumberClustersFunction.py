"""
#
# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo
#
# Código em Python para calcular o número de clusters para o algoritmo K-Means, mediante 
# dois métodos que são utilizados para a avaliação do número apropriado de clusters:
# - Método do cotovelo (The elbow method)
# - Coeficiente de silueta (The silhouette coefficient)
#
# O código faz o cálculo do coeficiente de silueta (average silhouette coefficient) e
# o cálculo da suma do erro quadrático (sum of the squared error - SSE).
# 
# INPUT:
# - data: numpy array multivariada
# 
# OUTPUT:
# - silhouette_coefficients: Lista com os valores (scores) do coeficiente de silueta
# - sse: Lista com os valores (scores) do cálculo da suma do erro quadrático
#
*** Script baseado no Blog Real Python
*** Link: https://realpython.com/k-means-clustering-python/
#
"""

# -------------------------------------------------------------------------------------------
from random import sample
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MaxAbsScaler
from kneed import KneeLocator

# Definindo a função para avaliar o número de clusters
def number_clusters_KMeans(data, silhouette = False, SSE = True):

    # INPUT
    #
    # data: Numpy array multivariado com as características dos parâmetros harmônicos
    #       ppmean, Amplitude Normalizada e fase (LST) do 1º e 2º harmônico (6 variáveis)
    #       * ppmean: precipitação média das 24 hóras
    #       * LST: Local Solar Time
    #
    # OUTPUT
    #
    # - silhouette_coefficients: valores (scores) do coeficientes de silueta
    # - sse: valores (scores) da suma do erro quadrático  
    #
    #  ------------------------------------------------------------------------------------------------------- 
    #
    # Fazendo um Pipeline para o pre-processamento dos dados
    # MaxAbsScaler() <- Scala os dados de 0 - 1, dividindo os dados com o valor máximo de cada característica
    # PCA(n_componentes = x) <- Reduz a dimensionalidade dos arrays como uma combinação linear do número de
    #                           componentes estabelecida na função PCA

    preprocessor = Pipeline(
        [
            ("scaler", MaxAbsScaler()),
            ("pca", PCA(n_components = 2)),
        ]
    )

    # Parâmetros da função K-Means
    kmeans_kwargs = {
        "init":"k-means++",
        "n_init":50,
        "max_iter":500,
    }

    # Escalando data de [0 - 1] e reduzindo sua dimensionalidade em duas componentes do PCA
    preprocessed_data = preprocessor.fit_transform(data)

    # ---------------------------------------------------------------------------------------------------

    if silhouette == True:

        # Calculando o coeficiente de silueta (silhouette coefficients)

        # Lista para armazenar os valores médios do coeficiente de silueta de todas as amostras
        # Este valor vai dar uma perspectiva da densidade e separação dos clusters formados
        silhouette_avg = []

        for k in range(2,12):

            kmeans = KMeans(n_clusters = k, **kmeans_kwargs)
            kmeans.fit(preprocessed_data)

            score = silhouette_score(
                preprocessed_data,
                kmeans.labels_,
            )

            silhouette_avg.append(score)

            return silhouette_avg
        
    # --------------------------------------------------------------------------------------------
    if SSE == True:

        # Calculando a suma do erro quadrático (SSE)

        # Lista para armazenar os valores (scores) da suma do erro quadrático
        sse = []

        for k in range(1,12):

            kmeans = KMeans(n_clusters = k, **kmeans_kwargs)
            kmeans.fit(preprocessed_data)
            sse.append(kmeans.inertia_)
    
        return sse
