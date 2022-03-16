# ---------------------------------------------------------------------------
"""
#
# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo
#
# File: plots_KMeans.py
# Código em python para fazer os plots dos cluster obtidos com o
# algoritmo K-Means sob a Bacia Amazônica para os períodod de 
# DJF (6 clusters), MAM (6 clusters), JJA (6clusters) e SON(7 clusters)
#
"""
# --------------------------------------------------------------------------

# Livrarias de leitura de dados
print("1. Read packages")
from netCDF4 import Dataset
import xarray as xr
# Livrarias de cálculos
import numpy as np
import pandas as pd
# Livrarias para fazer os plots
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# Livrarias para agregar as projeções dos mapas e shapefiles
import cartopy,cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
import salem
print("2. End packages")
#
# -------------------------------------------------------------------------------------
# 
# Read of dataset 
print("3. Read dataset")
file_in = '/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_JJA.nc'
ds = salem.open_xr_dataset(file_in)
print("4. Open dataset ")

# -------------------------------------------------------------------------------------
# 
# Fazendo o plot
print("4. Inicializando o plot")

print("5. Criando a figura onde fazer o plot com projeção PlateCarre()")
fig, ax = plt.subplots(figsize=(16,7), subplot_kw = {'projection': ccrs.PlateCarree()})

# Estabelecendo os límites e intervalos dos eixos longitude (x) e latitude (y)
print("6. Estabelecendo os límites e intervalos dos eixos")
xticks = np.arange(-90, -49, 5)
yticks = np.arange(-25,10,5)

# Agrenado os límites e intervalos dos eixos de longitude e latitude
print("7. Agregando límites e projeção PlateCarree() ao plot")
ax.set_xticks(xticks, crs = ccrs.PlateCarree())
ax.set_yticks(yticks, crs = ccrs.PlateCarree())
# Formtando no estilo de Longitude e Latitude
print("8. Formatando o estilo dos eixos no formato Longitude e Latitude")
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
# Agregando linhas de grade no plot
print("9. Agregando linhas de grade")
ax.grid(c='k', ls='-', alpha=0.3)

# Agregando linhas de costa
print("10. Agregando linhas de costa")
ax.coastlines('50m')
# Agregando os rios na Bacia Amazônica
print("11. Agregando os rios da Bacia Amazônica")
rivers_50m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m')
ax.add_feature(rivers_50m, facecolor = 'None', edgecolor = 'b', linewidth = 1)
# Agregando as Bordas dos límites dos paises 
print("12. Agregando os límites dos países")
ax.add_feature(cfeature.BORDERS)
# Agregando os estados do Brasil
print("13. Agregando os estados do Brasil")
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
)
ax.add_feature(states_provinces, edgecolor = '0.25')

# Agregando o shapefile da Bacia Amazônica
print("14. Agregando o Shapefile da Bacia Amazônica")
fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())
ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='black', facecolor='None', alpha=1,linewidth=1)

# Estabelecendo o rando de valores da paleta de cores
print("15. Estabelecendo o rando de valores da paleta de cores")
# Para DJF, MAM e JJA
colorb = np.arange(-0.5,6,1)
# Para SON
#colorb = np.arange(-0.5,7,1)

# Fazendo plot no estilo contour para delimitar os clusters
print("16. Fazendo o plot no estilo contour dos predicted_clusters")
cf = ax.contourf(ds.lon, ds.lat, ds['predicted_cluster'], levels=colorb, cmap='BrBG')

# Fazendo um achurado de '*' dos pixels com Amplitude Normalizada > 0.5 para ver ciclo diurno predominante de 24 h
# Segundo o criterio de Easterling e Robinson (1985)
print("17. Agregando um marcador '*' nos pixel com Amplitude Normalizada > 0.5")
ax.contourf(ds['lon'], ds['lat'], ds['C1_24h'] >= 0.5, colors='none', hatches='*', levels=[0.6,1.5])

# Agregando um título para o plot
print("18. Agrendo título do plot")
ax.set_title('Clusters da Bacia Amazônica - Período: JJA\n(*):Amplitude Normalizada > 0.5', size = 18)
# Agregando a paleta de cores com os valores centrados entre os intervalos colorb + 0.5
print("19. Agregando paleta de cores com valores centrados")
cbar=plt.colorbar(cf,ticks=colorb + 0.5, label='Clusters')
# Fazendo uma mudança para pôr labels na paleta de cores com os nomes dos clusters
print("20. Agregando labels à paleta de cores")
# Para DJF, MAM e JJA
cbar.set_ticklabels(["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","g"]) 
# Para SON
#cbar.set_ticklabels(["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","Cluster 7","g"]) 

# Agregando legenda para (*)
print("21. Agregando legenda para a (*) indicador da An > 0.5")
ax.legend(['(*): AN > 0.5'], bbox_to_anchor = (1.4, .01), frameon = True, loc='upper right', prop={'size':14})

# Salvando a figura np formato .png
print("22. Salvando a figura no formato .png")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/clusters_JJA_BA.png', format='png', dpi = 100)
print("23. Figura salvada")

plt.show()
print("Execução finalizada")