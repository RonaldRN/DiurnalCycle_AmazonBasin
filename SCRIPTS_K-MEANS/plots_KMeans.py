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
file_DJF = '/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_DJF.nc'
file_MAM = '/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_MAM.nc'
file_JJA = '/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_JJA.nc'
file_SON = '/home/ronaldrn/ronald/mestrado/NETCDF_K-MEANS_BA/BA_K-Means_SON.nc'

print('4. Ler o dado de topografia')
ds_topo = xr.open_dataset('/home/ronaldrn/ronald/mestrado/topography/topo_23.1.nc')
# Fazendo um slice para a Área da Bacia Amazônica
print('5. Fazer um slice do dataset de topografia centrado na Amazônia')
ds_topo_ba = ds_topo.sel(lat=slice(-25, 10), lon=slice(-85, -45))

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

# Inserir o período de interese  
periodo = input("Digite o código do período em upper-case letters: ")
print('                                                                    ')
print("6. Ler datasets")

if periodo == 'DJF':
    ds = salem.open_xr_dataset(file_DJF)
    # Labels da paleta de cores
    clusters = ["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","g"]
    # Rango de valores da paleta de cores
    colorb = np.arange(-0.5,6,1)

elif periodo == 'MAM':
    ds = salem.open_xr_dataset(file_MAM)
    # Labels da paleta de cores
    clusters = ["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","g"]
    # Rango de valores da paleta de cores
    colorb = np.arange(-0.5,6,1)

elif periodo == 'JJA':
    ds = salem.open_xr_dataset(file_JJA)
    # Labels da paleta de cores
    clusters = ["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","g"]
    # Rango de valores da paleta de cores
    colorb = np.arange(-0.5,6,1)

elif periodo == 'SON':
    ds = salem.open_xr_dataset(file_SON)
    # Labels da paleta de cores
    clusters = ["Cluster 1","Cluster 2","Cluster 3","Cluster 4","Cluster 5","Cluster 6","Cluster 7","g"]
    # Rango de valores da paleta de cores
    colorb = np.arange(-0.5,7,1)

# -------------------------------------------------------------------------------------
# 
# Fazendo o plot
print("7. Inicializando o plot")

print("8. Criando a figura onde fazer o plot com projeção PlateCarre()")
fig, ax = plt.subplots(figsize=(10,10), subplot_kw = {'projection': ccrs.PlateCarree()})

# Estabelecendo os límites e intervalos dos eixos longitude (x) e latitude (y)
print("9. Estabelecendo os límites e intervalos dos eixos")
xticks = np.arange(-90, -49, 5)
yticks = np.arange(-25,10,5)

# Agrenado os límites e intervalos dos eixos de longitude e latitude
print("10. Agregando límites e projeção PlateCarree() ao plot")
ax.set_xticks(xticks, crs = ccrs.PlateCarree())
ax.set_yticks(yticks, crs = ccrs.PlateCarree())
# Editando o tamanho dos labels dos eixos da longitude e latitude
ax.set_xticklabels(xticks, fontsize = 16)
ax.set_yticklabels(yticks, fontsize = 16)
# Formtando no estilo de Longitude e Latitude
print("11. Formatando o estilo dos eixos no formato Longitude e Latitude")
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
# Agregando linhas de grade no plot
print("12. Agregando linhas de grade")
ax.grid(c='k', ls='-', alpha=0.3)

# Agregando linhas de costa
print("13. Agregando linhas de costa")
ax.coastlines('50m')
# Agregando os rios na Bacia Amazônica
print("14. Agregando os rios da Bacia Amazônica")
rivers_50m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m')
ax.add_feature(rivers_50m, facecolor = 'None', edgecolor = 'b', linewidth = 1)
# Agregando as Bordas dos límites dos paises 
print("15. Agregando os límites dos países")
ax.add_feature(cfeature.BORDERS)
# Agregando os estados do Brasil
print("16. Agregando os estados do Brasil")
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
)
ax.add_feature(states_provinces, edgecolor = '0.25')

# Agregando o shapefile da Bacia Amazônica
print("17. Agregando o Shapefile da Bacia Amazônica")
fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())
ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor = 'black', facecolor = 'None', alpha =1 ,linewidth = 1)

# Fazendo plot no estilo contour para delimitar os clusters
print("18. Fazendo o plot no estilo contour dos predicted_clusters")
cf = ax.contourf(ds.lon, ds.lat, ds['predicted_cluster'], levels = colorb, cmap = 'BrBG')

# Fazendo um achurado de '*' dos pixels com Amplitude Normalizada > 0.5 para ver ciclo diurno predominante de 24 h
# Segundo o criterio de Easterling e Robinson (1985)
print("19. Agregando um marcador '*' nos pixel com Amplitude Normalizada > 0.5")
ax.contourf(ds['lon'], ds['lat'], ds['C1_24h'] >= 0.5, colors = 'none', hatches = ['**'], levels = [0.6,1.5])

ax.contourf(ds['lon'], ds['lat'], ds['ppmean'] <= 0.01, colors = 'red', hatches = ['XX'], levels = [0.6,1.5])

# Agregando um título para o plot
print("20. Agrendo título do plot")
ax.set_title('Clusters da Bacia Amazônica - Período: ' + f'{periodo}\n(*):Amplitude Normalizada > 0.5', size = 22)
# Agregando a paleta de cores com os valores centrados entre os intervalos colorb + 0.5
print("21. Agregando paleta de cores com valores centrados")
cbar=plt.colorbar(cf, ticks = colorb + 0.5, label = 'Clusters', fraction = 0.047)
# Fazendo uma mudança para pôr labels na paleta de cores com os nomes dos clusters
print("22. Agregando labels à paleta de cores")
# Para DJF, MAM , JJA e sON
cbar.set_ticklabels(clusters) 

# Agregando legenda para (*)
print("23. Agregando legenda para a (*) indicador da An > 0.5")
#ax.legend(['(*): AN > 0.5'], bbox_to_anchor = (1.4, .01), frameon = True, loc = 'upper right', prop = {'size':14})

# Topografia
#print("24. Agregando o contorno de 1500m de altitude")
#colorb = np.arange(1500,1550,50)
#cb = ax.contour(ds_topo_ba.lon, ds_topo_ba.lat, ds_topo_ba['z'], levels = colorb, colors = ['brown'], linewidths=0.75)

# Para deixar menos espaço em branco
fig.tight_layout

plt.show()

# Salvando a figura np formato .png
print("25. Salvando a figura no formato .png")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_KMEANS/clusters_' + f'{periodo}_BA.png', format='png', dpi = 300)
print("26. Figura salvada")

print("27. Execução finalizada")