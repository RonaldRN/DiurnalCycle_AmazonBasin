"""

Author: Ronald Guiuseppi Ramírez Nina
e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
Estudante de Mestrado
Departamento de Ciências Atmosféricas IAG - USP
Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Pauo

File: k-means_diurnal_cycle.py
Código em Python para fazer o K-Means Clustering aplicados à
Bacia Amazônica para regionalizar as áreas homogêneas do 
ciclo diurno da precipitação, utilizando como inputs os parâmetros
da Análise Harmônica (1º e 2º):

INPUTS
- ppmean: precipitação média do dia
- An : Amplitude normalizada do 1º e 2º harmônico
        An =  Amplitude
             -----------
                ppmean
- Fase do 1º e 2º harmônica (Local Solar Time)

OUTPUTS
- component_1: Primeira componente do PCA
- component_2: Segunda componente do PCA
- predicted_clusters: Labels dos clusters estabelecidos pelo K-Means

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
file_in = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_JJA.nc"

# Read of dataset
print("4. Abrindo o file netcdf com os parâmetros harmônicos")
ds = xr.open_dataset(file_in)

#-------------------------------------------------------------------------------------------------

# Converter dataset xarray para DataFrame de Pandas
print("5. Convertendo o arquivo netCDF (xarray) para DataFrame de Pandas")
params_df = ds.to_dataframe()

# Fazendo uma copia do params_df
params_df1 = params_df
print("6. Removendo os valores NaN e reseteando o index do DataFrame")
params_df1 = params_df1.dropna().reset_index() # delete NaN and reset index
print("7. Removendo a primeira coluna do index anterior")

#------------------------------------------------------------------------------------------------------

# Salvando o DataFrame como arquivo .csv
print("8. Salvando o DataFrame params_df com formato .csv e separador ',' ")
params_df1.to_csv('harmonic_params.csv', sep = ',')

# Abrindo o arquivo .csv com os dados dos parâmetros da análise harmônica
# A função KMeans aceita como input um array
print("9. Fazendo o path do arquivo harmonic_params.csv")
datafile = "harmonic_params.csv" # Path of file .csv
# Abrindo o arquivo .csv com o pacote numpy
print("10. Abrindo o arquivo .csv, e formatando só os valores no tipo array")
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
print("11. Criando um Pipeline para o pre-processamento dos dados")
preprocessor = Pipeline(
    [
        ("scaler", MaxAbsScaler()),
        ("pca", PCA(n_components = 2)),
    ]
)

# Fazendo um Pipeline para a aplicação do algoritmo K-Means, estabelecendo os parâmetros da função KMeans
print("12. Fazendo um Pipeline para o algoritmo do K-Means")
clusterer = Pipeline(
    [
        (
            "kmeans",
            KMeans(
                n_clusters = 6,
                init = "k-means++",
                n_init = 50,
                max_iter = 500,
            )
        )
    ]
) 

# Fazendo um Pipeline com a combinação das duas Pipelines de pre-processamento e K-Means
print("13. Pipeline emcadenando com os Pipeline de pre-processamento e K-Means")
pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("clusterer", clusterer)
    ]
)

#--------------------------------------------------------------------------------------------

# Executando o Pipeline
print("14. Executando o Pipeline")
pipe.fit(data)

# Extraíndo os outputs das componentes 1 e 2 
print("15. Executando o pipeline de pre-processamento")
preprocessed_data = pipe["preprocessor"].transform(data)

# Extraindo os predicted_labels
print("16. Executando o Pipeline do K-Means")
predicted_labels = pipe["clusterer"]["kmeans"].labels_

# Criando um DataFrame com as componentes do PCA e os predicted cluster do K-Means
print("17. Criando um DataFrame para armazenar as Componentes 1º e 2º e os predicter clusters")
pcadf = pd.DataFrame(
    preprocessed_data,
    columns = ["component_1", "component_2"],
)

pcadf["predicted_cluster"] = predicted_labels

# Agrenado as componentes do PCA e os predicted cluster no params_df
print("18. Criando as colunas para agregar as componentes 1º e 2º e os predicted_clusters")
params_df1["component_1"] = pcadf["component_1"]
params_df1["component_2"] = pcadf["component_2"]
params_df1["predicted_cluster"] = pcadf["predicted_cluster"]

# Convertir o DataFrame para um arquivo NetCDF
# Fazendo o index do DataFrame params_df com a 'lat' e 'lon'
print("19. Criando index do DataFrame com as latitudes e longitudes")
params_df1.set_index(["lat", "lon"], inplace = True)

# Retornando as componentes do PCA e o predicted_cluster para o params_df (DataFrame original)
params_df["component_1"] = params_df1["component_1"]
params_df["component_2"] = params_df1["component_2"]
params_df['predicted_cluster'] = params_df1["predicted_cluster"]

# Fazendo a conversão do DataFrame para NetCDF
print("20. Convertendo o DataFrame para um xarray (NetCDF)")
kmeans_nc = params_df.to_xarray()
# Escrevendo a projeção para o arquivo NetCDF
print("21. Escrevendo a projeção epsg:4326 <- WGS 84")
kmeans_nc.rio.write_crs('epsg:4326', inplace = True)
# Salvando o arquivo netcdf
print("22. Salavando o arquivo em formato NetCDF com os Predicted Cluster")
kmeans_nc.to_netcdf('/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_JJA.nc')
print("23. Arquivo NetCDF salvado")

#---------------------------------------------------------------------------------

# fazendo um prin das componentes do PCA
plt.style.use("fivethirtyeight")
plt.figure(figsize=(8, 8))

scat = sns.scatterplot(
    "component_1",
    "component_2",
    s=50,
    data=pcadf,
    hue="predicted_cluster",
    #style="true_label",
    palette="Set2",
)

scat.set_title(
    "Clustering results from Params Harmonic of\nDiurnal Cycle of Precipitation"
)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)

plt.show()