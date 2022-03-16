"""

Author: Ronald Guiuseppi Ramírez Nina
e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
Estudante de Mestrado
Departamento de Ciências Atmosféricas IAG - USP
Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Pauo

File: clusters_k-means.py
Código em Python para fazer os métodos do coeficiente de silueta
e o método do cotovelo para o K-Means Clustering aplicados à
Bacia Amazônica para regionalizar as áreas homogêneas do 
ciclo diurno da precipitação, utilizando como inputs os parâmetros
da Análise Harmônica (1º e 2º):

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
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MaxAbsScaler
from kneed import KneeLocator

# Importando a Função
from NumberClustersFunction import number_clusters_KMeans

# Importando pacotes de plotagem
import seaborn as sns
import matplotlib.pyplot as plt
print("2. Terminou de importar os pacotes (packages)")

#------------------------------------------------------------------------------------------------

print("3. Path of file")
# Path of files
file_in = "/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_DJF.nc"

# Read of dataset
print("4. Abrindo o file netcdf com os parâmetros harmônicos")
ds = xr.open_dataset(file_in)

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
params_df.to_csv('harmonic_params.csv', sep = ',')

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

# Executando a função number_clusters_KMeans
print("11. Executando a função NumberClustersFunction.py")
silhouette_coefficients, sse = number_clusters_KMeans(data)
print("12. Salvando os scores do coeficiente de silueta e sse")

# --------------------------------------------------------------------------------------------------

# Fazendo os plot dos scores do coeficiente de silueta e sse 
print("13. Fazendo os plot dos scores do coeficiente de silueta e sse")
fig = plt.figure(figsize = (14,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(range(2,12), silhouette_coefficients, color = 'C0', lw = 2, label='Silhouette coefficient')
ax2.plot(range(1,12), sse, color = 'C1', lw = 2, label = 'Sum of the squared error (SSE)')

ax1.set_title('The silhouette coefficiente - DJF')
ax1.set_xlabel('Number of Clusters')
ax1.set_ylabel('Silhouette coefficien scores')
ax1.set_xticks(range(2,12,1))
ax1.legend(loc = 'upper right', frameon = False)

ax2.set_title('The elbow method - DJF')
ax2.set_xlabel('Number of Clusters')
ax2.set_ylabel('SSE scores')
ax2.set_xticks(range(1,12,1))
ax2.legend(loc = 'upper right', frameon = False)

fig.tight_layout()
plt.show()

print("14. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/Number_clusters_DJF_BA.png', format='png', dpi = 100)
print("15. Finalizou de executar o código")
