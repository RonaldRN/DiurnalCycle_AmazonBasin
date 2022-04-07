"""
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# MSc. Student at Institute of Astronomy, Geophisycs and Atmospheric Sciences at University of São Paulo
# File: diurnal_cycle_netcdf_BA.py 

######################################################3
# Descriptiopn:
# Esse script faz os gráficos dos parâmetros da Análise harmônico para a Bacia Amazônica

"""
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

#---------------------------------------------------------------------------------------------------

# Nome do arquivo
file_in = '/home/ronaldrn/ronald/mestrado/DADOS_PARAMETROS_HARMONICOS_AS/diurnal_cycle_MAM_AS.nc'
# Abrindo o arquivo NetCDF
print("3. Ler datasets")
ds = salem.open_xr_dataset(file_in)
print("4. Terminou de ler os datasets")

# Fazendo um mask para a Bacia Amazônica
# Lendo o shapefile da Bacia Amazônica
print("5. Ler o shapefile da Bacia Amazônica")
shp = salem.read_shapefile('/home/ronaldrn/ronald/mestrado/Amazonia_internacional_SIRGAS_2000/amazlm_poly_1608.shp')
shp_ba = shp.loc[shp.index == 3]
print("6. Terminou de ler o shapefile da Bacia Amazônica")
# Fazendo o clip com o shapefile da Bacia Amazônica
print("7. Fazendo o clip do arquivo netcdf com o shapefile da Bacia Amazônica")
dsr = ds.salem.roi(shape = shp_ba).sel(lat=slice(-25, 10), lon=slice(-82, -48))
print("8. Terminou de fazer o clip")

# A variável "ppmean" têm unidades de mm/0.5hour, já que é a média dos 48 registos (dt = 0.5hour) no dia
# Essa variável "ppmean" vai ser transformada com unidades de mm/hour na média de 24 horas com 24 registros
dsr['ppmean'] = dsr['ppmean'] * 2

# Salvando o arquivo com o mask da Bacia Amazônica
print('Salvando mask da Bacia Amazônica em arquivo NetCDF')
dsr.to_netcdf('/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_MAM.nc')
print("Terminou de salvar o arquivo NetCDF")
#
# ------------------------------------------------------------------------------------------------------------
#
# Agregar una imagen satelital de fondo
# Importando os para estabelecer o diretório de trabalho para a imagem de fondo
print("Importan uma imagem satelital de fondo")
print("Importando o pacote os")
import os as os
# Estabelcer o diretório para a imagem de fondo
print("Path do diretório de trabalho atual")
current_directory = os.getcwd()
# Configurando um environment variable
print("Configurando um environment variable")
os.environ["CARTOPY_USER_BACKGROUNDS"] = os.path.join(current_directory,'CARTOPY_IMGS')
os.getenv('CARTOPY_USER_BACKGROUNDS')
# Extenção da imagem
print("Extenção da imagem")
lat_min = -25 # Latitude mínima do plot
lat_max = 10  # LAtitude máxima do plot
lon_min = -82 # Longitude mínima do plot
lon_max = -48 # Longitude máxima do plot
extent = [lon_min, lon_max, lat_min, lat_max]
# Imagem de fondo para nosso plot
#ax.background_img(name='BM_NASA', resolution='low',extent=extent)

#------------------------------------------------------------------------------------------------------

# Criando un class para calcular os mid_points
print("9. Criando um class para calcular os mid points")
class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin, vmax, midpoint=0, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return np.ma.masked_array(np.interp(value, x, y))
print("10. Terminou de criar o class dos mid points")

#-------------------------------------------------------------------------------------------------------------

# Estabelecendo as características do gráfico
print("11. Criando figura para os plots")
fig = plt.figure(figsize = (18,10), dpi = 100) 
#plt.title('Parâmetros do Análise harmônico do Ciclo Diurno para o período DJF', size = 20)
plt.axis = ('off')
plt.subplots_adjust(wspace=0.3,hspace=0.0001)

# Para eliminar marco de la figura comple
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False) 
for pos in ['right', 'top', 'bottom', 'left']:
     plt.gca().spines[pos].set_visible(False)

#-------------------------------------------------------------------------------------------------------

# Nome das variáveis
vars = ['ppmean','C1_24h','F1_LST','C2_24h','F2_LST','F2_12h_LST']
# Nome dos subplots
axx = ['ax1','ax2','ax3','ax4','ax5','ax6']
# Título dos gráficos
title = ['a) 24 Hourly Precipitation Mean of MAM (mm/day)','b) Normalized Amplitude 1ºH MAM','c) Phase of the diurnal peak 1ºH MAM',\
    'd) Normalize Amplitude 2ºH MAM','e) Phase of the semi-diurnal peak 2ºH MAM','f) Phase of the semi-diurnal peak 2ºH MAM']
# Color map das paletas de cores
colors_map = ['BrBG','PuOr','hsv','plasma','RdGy','twilight_shifted']
# Nome dos paletas de cores
labels = ['Precipitation Mean (mm/day)','Ratio of Amp. to Mean of 1ºH','Local Solar Time do Max. [hour]',\
    'Ratio of Amp. to Mean of 2ºH','Local Solar Time do Max. [hour]','Local Solar Time do Max. [hour]']
# Valores para o mip_point das paletas de cores
mid_point = [0.275, 0.5, 12, 0.5, 6, 18]
# Nova paleta de cores para a fase do 1º harmônico
new_hsv = cm.get_cmap('hsv', 24)
boundaries = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
norm1 = matplotlib.colors.BoundaryNorm(boundaries, new_hsv.N, clip=True)
print("12. Terminou de estabelecer os parâmetros para as figuras")

print("13. Fazendo o loop para gerar as figuras dos parâmetros diurnos")
for i in range(1,7,1):
    # Fazendo os subplots com suas projeções
    axx[i-1] = fig.add_subplot(2,3,i, projection = ccrs.PlateCarree())
    # Agregando linhas de costa
    axx[i-1].coastlines('50m')
    # Formatando a latitude e longitude
    axx[i-1].xaxis.set_major_formatter(LongitudeFormatter())
    axx[i-1].yaxis.set_major_formatter(LatitudeFormatter())
    #
    # ------------------------------------------------------------------------------------------
    #
    # Agregando a imagem satelital de fondo
    axx[i-1].background_img(name='BM_NASA', resolution='low', extent=extent)
    #
    # -------------------------------------------------------------------------------------------
    #
    # Agregando linhas da grade
    gl = axx[i-1].gridlines(draw_labels = True)
    # Removendo os labels da grade do lado superior
    gl.top_labels = False
    # Removendo os labels da grade do lado direito
    gl.right_labels = False
    # Estabelendo o size dos labels no eixo X
    gl.xlabel_style = {'size': 8}
    # Estabelecendo o size dos labels no eixo Y
    gl.ylabel_style = {'size': 8}
    # Agregano os Rios importados do NaturalEarthFeature
    rivers_50m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m')
    axx[i-1].add_feature(rivers_50m, facecolor = 'None', edgecolor = 'b', linewidth = 1)
    # Agregando os paises
    axx[i-1].add_feature(cfeature.BORDERS, edgecolor='0.25')
    # Agregando Estados
    states_provinces = cfeature.NaturalEarthFeature(
        category = 'cultural',
        name = 'admin_1_states_provinces_lines',
        scale = '50m',
        facecolor = 'none')
    axx[i-1].add_feature(states_provinces, edgecolor = '0.25')
    # Agregando o shapefile da Bacia da Amazônia
    # Amazon Basin
    fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
    adm1_shapes = list(shpreader.Reader(fname).geometries())
    axx[i-1].add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='black', facecolor='none', alpha=1, linewidth = 1)
    # Definindo os valores máximos, mínimos e o mid_point das paletas de cores
    norm = MidpointNormalize(vmin = dsr[f'{vars[i-1]}'].min(), vmax = dsr[f'{vars[i-1]}'].max(), midpoint = mid_point[i-1])
    # Fazendo o plotagem para cada panel

    if i == 3:  # Editando a paleta de cores para a Fase do 1º Harmônico (norm = norm1)
        dsr[f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm1,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})
    else:       # Editando a paleta de cores considerando o ponto médio (norm = norm)
        dsr[f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})

    # Fazendo o plotagem para cada panel
    #ds[f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm,\
    #     transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.75})

    # Agrendo title aos paneis de cada subplot
    axx[i-1].set_title(f'{title[i-1]}', size = 10, fontweight = 'bold', fontfamily = 'sans')

    plt.subplots_adjust(hspace=0.2, wspace=0.1, left=0.125, bottom=0.1, right=0.9, top=0.9)

print("14. Figuras dos parâmetros diurnos")
plt.show()

print("15. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/OUTPUTS_PARAMETERS_DIURNAL_BA/Parameters_diurnal_cycle_MAM_BA.png', format='png', dpi = 100)

print("16. Finalizou de executar o código")
