"""

# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo

# File: clusters_k-means.py
# Código em Python para fazer os métodos dos scores de silueta
# e o método elbow para o obtenção do número ótima de clusters na
# aplicação da técnica K-Means Clustering aplicados à
# Bacia Amazônica para regionalizar as áreas homogêneas do 
# ciclo diurno da precipitação, utilizando como inputs os parâmetros
# da Análise Harmônica (1º e 2º): taxa de precipitação média (mm/h),
# amplitude normalizada e fase.

*** Script baseado no Blog Real Python
*** Link: https://realpython.com/k-means-clustering-python/

"""

# Importando Pacotes (packages)
print("RUN CODE")

print("1. Importando Pacotes (packages)")
# Importando pacotes de processamento de dados
import pandas as pd
import numpy as np
import xarray as xr
import rioxarray

# Importando pacotes de Machine Learning - K-Means
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MaxAbsScaler
from kneed import KneeLocator

# Importando a Função
from NumberClustersFunction import number_clusters_KMeans

# Importando pacotes de plotagem
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
print("2. Terminou de importar os pacotes (packages)")

#------------------------------------------------------------------------------------------------

print("3. Path of file")
# Path of files
file_DJF = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_DJF.nc"
file_MAM = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_MAM.nc"
file_JJA = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_JJA.nc"
file_SON = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_SON.nc"

# Abrindo o arquivo NetCDF
print("--------------------------------------------------------------------")
print('                                                                    ')
print("DIGITAR O CÓDIGO DO PERÍODO DE INTERESSE:")
print('                                                                    ')
print("DJF: Dezembro - Janeiro - Fevereiro (DJF)")
print("MAM: Março - Abril - Maio (MAM)")
print("JJA: Junho - Julho - Agosto (JJA)")
print("SON: Setembro - Novembro - Dezembro (SON)")
print('                                                                    ')

periodo = input("Digite o código do período em upper-case letters: ")
print('                                                                    ')
print("Ler dataset")

# Read of dataset
print("4. Abrindo o file netcdf com os parâmetros harmônicos")
if periodo == 'DJF':
    ds = xr.open_dataset(file_DJF)
    title_silhouette = 'a) The silhouette plot clusters - ' + f'{periodo}'
    title_elbow = 'a) Elbow method - ' + f'{periodo}'

elif periodo == 'MAM':
    ds = xr.open_dataset(file_MAM)
    title_silhouette = 'b) The silhouette plot clusters - ' + f'{periodo}'
    title_elbow = 'b) Elbow method - ' + f'{periodo}'

elif periodo == 'JJA':
    ds = xr.open_dataset(file_JJA)
    title_silhouette = 'c) The silhouette plot clusters - ' + f'{periodo}'
    title_elbow = 'c) Elbow method - ' + f'{periodo}'

elif periodo == 'SON':
    ds = xr.open_dataset(file_SON)
    title_silhouette = 'd) The silhouette plot clusters - ' + f'{periodo}'
    title_elbow = 'd) Elbow method - ' + f'{periodo}'

#-------------------------------------------------------------------------------------------------

# Converter dataset xarray para DataFrame de Pandas
print("5. Convertendo o arquivo netCDF (xarray) para DataFrame de Pandas")
params_df = ds.to_dataframe().reset_index() # reset index of lat and lon
print("6. Removendo os valores NaN e reseteando o index do DataFrame")
params_df = params_df.dropna().reset_index() # delete NaN and reset index
print("7. Removendo a primeira coluna do index anterior")
params_df = params_df.drop(params_df.columns[0], axis = 'columns') # Removendo columns[0] do index anterior

#------------------------------------------------------------------------------------------------------

# Salvando o DataFrame como arquivo .csv
print("8. Salvando o DataFrame params_df com formato .csv e separador ',' ")
params_df.to_csv('harmonic_params_' + f'{periodo}.csv', sep = ',')

# Abrindo o arquivo .csv com os dados dos parâmetros da análise harmônica
# A função KMeans aceita como input um array
print("9. Fazendo o path do arquivo harmonic_params.csv")
datafile = 'harmonic_params_' + f'{periodo}.csv' # Path of file .csv
# Abrindo o arquivo .csv com o pacote numpy
print("10. Abrindo o arquivo .csv, e formatando só os valores no tipo array")
data = np.genfromtxt(
    datafile,
    delimiter = ",",
    usecols = range(3,9),
    skip_header = 1
)

# Fazendo o pre-processamento da matrix de características (6), primeiro escalando os dados
# entre 0-1 e logo reduzir para duas características (PC1 e PC2)
preprocessor = Pipeline(
    [
        ("scaler", MaxAbsScaler()),
        ("pca", PCA(n_components = 2)),
    ]
)
#------------------------------------------------------------------------------------------------------

# Executando a função number_clusters_KMeans e obter SSE
print("11. Executando a função NumberClustersFunction.py")
sse = number_clusters_KMeans(data)
print("12. Salvando os scores do coeficiente de silueta e sse")

# Fazendo o pre-processamento dos dados para aplicar o algoritmo K-Means
preprocessed_data = preprocessor.fit_transform(data)

# --------------------------------------------------------------------------------------------------

# Fazendo os plot dos silhouette scores do coeficiente de silueta e sse 
print("13. Fazendo os plot dos scores do coeficiente de silueta e sse")

# Criando uma lista com o número de clusters
range_n_clusters = [2,3,4,5,6,7,8]

for n_clusters in range_n_clusters:
    fig, (ax1, ax2) = plt.subplots(1,2, figsize = (10,5))

    # O Silhouette coefficient varia entre -1 e +1
    ax1.set_xlim([-0.1, 1])
    # O (n_clusters + 1)*10 é para inserir espaço em branco entre os plots das silhouette dos clusters 
    ax1.set_ylim([0, len(preprocessed_data) + (n_clusters + 1) * 10])

    # Executamos o algoritmo K-Means
    clusterer = KMeans(n_clusters = n_clusters, init = "k-means++", n_init = 50, max_iter = 500)
    cluster_labels = clusterer.fit_predict(preprocessed_data)

    # O silhouette_score dá como resultado o valor médio de todas as amostras
    # Gera uma perspectiva da densidade e separação dos clusters formados
    silhouette_avg = silhouette_score(preprocessed_data, cluster_labels)
    # Calcula os silhouette scores para cada amostra
    sample_silhouette_values = silhouette_samples(preprocessed_data, cluster_labels)

    y_lower = 10

    for i in range(n_clusters):
        # Adicionar os silhouette scores para as amostras pertenecenetes a cada cluster 
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
        # Ordenar os silhouette scores de cada ckuster
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, 'Cluster ' + str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title(title_silhouette, size = 18)
    ax1.set_xlabel('Silhouette coefficient values', fontsize = 16)
    ax1.set_ylabel("Cluster label", fontsize = 16)

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    ax1.set_xticklabels([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1], fontsize = 16)

    # Fazendo o segundo plot com os valores do SSE (soma do erro quadrático - Método elbow)
    ax2.plot(range(1,12), sse, color = 'C1', lw = 2, label = 'Sum of the squared error (SSE)', marker = 'o')
    ax2.axvline(x = n_clusters, color = 'red', linestyle = '--')
    ax2.set_title(title_elbow, size = 18)
    ax2.set_xlabel('Number of Clusters', fontsize = 16)
    ax2.set_ylabel('SSE scores', fontsize = 16)
    ax2.set_xticks(range(1,12,1))
    ax2.set_xticklabels(range(1,12,1), fontsize = 16)
    ax2.legend(loc = 'upper right', frameon = False)

    fig.tight_layout()
    # Salvando a figura
    fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/Number_clusters_' + f'{n_clusters}-' + f'{periodo}_BA.png',\
         format='png', dpi = 300)

plt.show()

print("14. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/Number_clusters_' + f'{periodo}_BA.png', format='png', dpi = 100)
print("15. Finalizou de executar o código")
