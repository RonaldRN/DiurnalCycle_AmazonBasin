"""
#
# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo
#
# File: k-means_diurnal_cycle.py
# Código em Python para fazer o K-Means Clustering aplicados à
# Bacia Amazônica para regionalizar as áreas homogêneas do 
# ciclo diurno da precipitação, utilizando como inputs os parâmetros
# da Análise Harmônica (1º e 2º). Também realiza os plots da aplicação
# da técnica K-Means no espaço do PCA (Análise de Componentes principais):
# 
# INPUTS
# - ppmean: precipitação média do dia
# - An : Amplitude normalizada do 1º e 2º harmônico
#        An =  Amplitude
#             -----------
#                ppmean
# - Fase do 1º e 2º harmônica (Local Solar Time)
#
# OUTPUTS
# - component_1: Primeira componente do PCA
# - component_2: Segunda componente do PCA
# - predicted_clusters: Labels dos clusters estabelecidos pelo K-Means
#
*** Script baseado no Blog Real Python
*** Link: https://realpython.com/k-means-clustering-python/
#
"""

# Importando Pacotes (packages)
print("RUN CODE")

print("1. Importando Pacotes (packages)")
# Importando pacotes de processamento de dados
import pandas as pd
import numpy as np
import xarray as xr
import rioxarray
import salem

# Importando pacotes de Machine Learning - K-Means
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MaxAbsScaler
from kneed import KneeLocator

# Importando pacotes de plotagem
import seaborn as sns
import matplotlib.pyplot as plt
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
    n_cluster = 6
    legend_map = {0:'Grupo 1', 1:'Grupo 2', 2:'Grupo 3', 3:'Grupo 4', 4:'Grupo 5', 5:'Grupo 6'}
    title = 'a)Clustering results from Params Harmonic of\nDiurnal Cycle of Precipitation - ' + f'{periodo}'

elif periodo == 'MAM':
    ds = xr.open_dataset(file_MAM)
    n_cluster = 6
    legend_map = {0:'Grupo 1', 1:'Grupo 2', 2:'Grupo 3', 3:'Grupo 4', 4:'Grupo 5', 5:'Grupo 6'}
    title = 'b)Clustering results from Params Harmonic of\nDiurnal Cycle of Precipitation - ' + f'{periodo}'

elif periodo == 'JJA':
    ds = xr.open_dataset(file_JJA)
    n_cluster = 6
    legend_map = {0:'Grupo 1', 1:'Grupo 2', 2:'Grupo 3', 3:'Grupo 4', 4:'Grupo 5', 5:'Grupo 6'}
    title = 'c)Clustering results from Params Harmonic of\nDiurnal Cycle of Precipitation - ' + f'{periodo}'

elif periodo == 'SON':
    ds = xr.open_dataset(file_SON)
    n_cluster = 7
    legend_map = {0:'Grupo 1', 1:'Grupo 2', 2:'Grupo 3', 3:'Grupo 4', 4:'Grupo 5', 5:'Grupo 6', 6:'Grupo 7'}
    title = 'd)Clustering results from Params Harmonic of\nDiurnal Cycle of Precipitation - ' + f'{periodo}'

print("5. Terminou de ler o dataset")

#-------------------------------------------------------------------------------------------------
# Converter dataset xarray para DataFrame de Pandas
print("6. Convertendo o arquivo netCDF (xarray) para DataFrame de Pandas")
params_df = ds.to_dataframe()

# Fazendo uma copia do params_df
params_df1 = params_df
print("7. Removendo os valores NaN e reseteando o index do DataFrame")
# Delete NaN and reset index
params_df1 = params_df1.dropna().reset_index() 
print("8. Removendo a primeira coluna do index anterior")

#------------------------------------------------------------------------------------------------------

# Salvando o DataFrame como arquivo .csv
print("9. Salvando o DataFrame params_df com formato .csv e separador ',' ")
params_df1.to_csv('harmonic_params_' + f'{periodo}.csv', sep = ',')

# Abrindo o arquivo .csv com os dados dos parâmetros da análise harmônica
# A função KMeans aceita como input um array
print("10. Fazendo o path do arquivo harmonic_params.csv")
datafile = 'harmonic_params_' + f'{periodo}.csv' # Path of file .csv
# Abrindo o arquivo .csv com o pacote numpy
print("11. Abrindo o arquivo .csv, e formatando só os valores no tipo array")
data = np.genfromtxt(
    datafile,
    delimiter = ",",
    usecols = range(3,9),
    skip_header = 1
)

#------------------------------------------------------------------------------------------------------

# Fazendo um Pipeline para o pre-processamento dos dados
# MaxAbsScaler() <- Scala os dados de 0 - 1, dividindo os dados com o valor máximo de cada característica
# PCA(n_componentes = x) <- Reduz a dimensionalidade dos arrays como uma combinação linear do número de
#                           componentes estabelecida na função PCA
print("12. Criando um Pipeline para o pre-processamento dos dados")
preprocessor = Pipeline(
    [
        ("scaler", MaxAbsScaler()),
        ("pca", PCA(n_components = 2)),
    ]
)

# Fazendo um Pipeline para a aplicação do algoritmo K-Means, estabelecendo os parâmetros da função KMeans
print("13. Fazendo um Pipeline para o algoritmo do K-Means")
clusterer = Pipeline(
    [
        (
            "kmeans",
            KMeans(
                n_clusters = n_cluster,
                init = "k-means++",
                n_init = 50,
                max_iter = 500,
            )
        )
    ]
) 

# Fazendo um Pipeline com a combinação das duas Pipelines de pre-processamento e K-Means
print("14. Pipeline emcadenando com os Pipeline de pre-processamento e K-Means")
pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("clusterer", clusterer)
    ]
)

#--------------------------------------------------------------------------------------------

# Executando o Pipeline
print("15. Executando o Pipeline")
pipe.fit(data)

# Extraíndo os outputs das componentes 1 e 2 
print("16. Executando o pipeline de pre-processamento")
preprocessed_data = pipe["preprocessor"].transform(data)

# Extraindo os predicted_labels
print("17. Executando o Pipeline do K-Means")
predicted_labels = pipe["clusterer"]["kmeans"].labels_

# Criando um DataFrame com as componentes do PCA e os predicted cluster do K-Means
print("18. Criando um DataFrame para armazenar as Componentes 1º e 2º e os predicter clusters")
pcadf = pd.DataFrame(
    preprocessed_data,
    columns = ["component_1", "component_2"],
)
# Salvando os labels dos clusters no DataFrame
pcadf["predicted_cluster"] = predicted_labels

# Agrenado as componentes do PCA e os predicted cluster no params_df
print("19. Criando as colunas para agregar as componentes 1º e 2º e os predicted_clusters")
params_df1["component_1"] = pcadf["component_1"]
params_df1["component_2"] = pcadf["component_2"]
params_df1["predicted_cluster"] = pcadf["predicted_cluster"]

# Convertir o DataFrame para um arquivo NetCDF
# Fazendo o index do DataFrame params_df com a 'lat' e 'lon'
print("20. Criando index do DataFrame com as latitudes e longitudes")
params_df1.set_index(["lat", "lon"], inplace = True)

# Retornando as componentes do PCA e o predicted_cluster para o params_df (DataFrame original)
params_df["component_1"] = params_df1["component_1"]
params_df["component_2"] = params_df1["component_2"]
params_df['predicted_cluster'] = params_df1["predicted_cluster"]

# Fazendo a conversão do DataFrame para NetCDF
print("21. Convertendo o DataFrame para um xarray (NetCDF)")
kmeans_nc = params_df.to_xarray()
# Escrevendo a projeção para o arquivo NetCDF
print("22. Escrevendo a projeção epsg:4326 <- WGS 84")
kmeans_nc.rio.write_crs('epsg:4326', inplace = True)
# Salvando o arquivo netcdf
print("23. Salavando o arquivo em formato NetCDF com os Predicted Cluster")
#kmeans_nc.to_netcdf('/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_' + f'{periodo}.nc')
print("24. Arquivo NetCDF salvado")

# Extraindo valores das duas primeiras Componentes Principais (PC)
print(pipe["preprocessor"]["pca"].explained_variance_ratio_)
# Salvando os valores das componentes principais
pcs = pipe["preprocessor"]["pca"].explained_variance_ratio_
# Salvando a variança da PC1
pc1 = round(pcs[0]*100,1)
# Salvanda a variança da PC2
pc2 = round(pcs[1]*100,1)

#---------------------------------------------------------------------------------

# fazendo um prin das componentes do PCA
#plt.style.use("fivethirtyeight")
fig = plt.figure(figsize = (8,8), dpi = 100) 

#plt.figure(figsize=(8, 8))

scat = sns.scatterplot(
    "component_1",
    "component_2",
    s=50,
    data=pcadf,
    hue=pcadf["predicted_cluster"].map(legend_map),
    palette="Set2",
    legend='full'
)

scat.set_title(title, fontweight = 'bold', fontfamily = 'sans', size = 18)

plt.xlabel('PC1 ' + f'({pc1}%)', size = 18)
plt.ylabel('PC2 ' + f'({pc2}%)', size = 18)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.legend(bbox_to_anchor = (0.82, 0.995), loc=2, borderaxespad=0.0)
# Ajustando os plots
fig.tight_layout()

plt.show()

# Salvando a figura
print("25. Salvando Figuras")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/PrincipalComponents_' + f'{periodo}_BA.png', format='png', dpi = 300)

print("Terminor de executar o código")

