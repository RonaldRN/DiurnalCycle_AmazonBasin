"""
#
# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo
#
# File: diurnal_cycle_netcdf_AS.py
# Código em Python para fazer plots dos parâmetros harmônicos sobre América do Sul: 
# taxa de precipitação média (mm/h), amplitude normalizada e fase do
# primeiro harmônico (1ºH) e segundo harmônico (2ºH).
#
"""

print("EXECUNTANDO O CÓDIGO")

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
print("2. Finished packages")
#---------------------------------------------------------------------------------------------------
# Nome do arquivo e pathfile
file_DJF = '/home/ronaldrn/ronald/mestrado/DADOS_PARAMETROS_HARMONICOS_AS/diurnal_cycle_DJF_AS.nc'
file_MAM = '/home/ronaldrn/ronald/mestrado/DADOS_PARAMETROS_HARMONICOS_AS/diurnal_cycle_MAM_AS.nc'
file_JJA = '/home/ronaldrn/ronald/mestrado/DADOS_PARAMETROS_HARMONICOS_AS/diurnal_cycle_JJA_AS.nc'
file_SON = '/home/ronaldrn/ronald/mestrado/DADOS_PARAMETROS_HARMONICOS_AS/diurnal_cycle_SON_AS.nc'

print('Ler o dado de topografia')
ds_topo = xr.open_dataset('/home/ronaldrn/ronald/mestrado/topography/topo_23.1.nc')
# Fazendo um slice para a Área da Bacia Amazônica
print('Fazer um slice do dataset de topografia centrado em AS')
ds_topo_ba = ds_topo.sel(lat=slice(-55, 12), lon=slice(-81, -35))

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
print("3. Ler datasets")

if periodo == 'DJF':
    ds = xr.open_dataset(file_DJF)
    # Título dos gráficos
    title = ['a) 24 Hourly Precipitation Mean of DJF (mm/day)','b) Normalized Amplitude 1ºH DJF','c) Phase of the diurnal peak 1ºH DJF',\
        'd) Normalize Amplitude 2ºH DJF','e) Phase of the semi-diurnal peak 2ºH DJF','f) Phase of the semi-diurnal peak 2ºH DJF']

elif periodo == 'MAM':
    ds = xr.open_dataset(file_MAM)
    # Título dos gráficos
    title = ['a) 24 Hourly Precipitation Mean of MAM (mm/day)','b) Normalized Amplitude 1ºH MAM','c) Phase of the diurnal peak 1ºH MAM',\
        'd) Normalize Amplitude 2ºH MAM','e) Phase of the semi-diurnal peak 2ºH MAM','f) Phase of the semi-diurnal peak 2ºH MAM']

elif periodo == 'JJA':
    ds = xr.open_dataset(file_JJA)
    # Título dos gráficos
    title = ['a) 24 Hourly Precipitation Mean of JJA (mm/day)','b) Normalized Amplitude 1ºH JJA','c) Phase of the diurnal peak 1ºH JJA',\
        'd) Normalize Amplitude 2ºH JJA','e) Phase of the semi-diurnal peak 2ºH JJA','f) Phase of the semi-diurnal peak 2ºH JJA']

elif periodo == 'SON':
    ds = xr.open_dataset(file_SON)
    # Título dos gráficos
    title = ['a) 24 Hourly Precipitation Mean of SON (mm/day)','b) Normalized Amplitude 1ºH SON','c) Phase of the diurnal peak 1ºH SON',\
        'd) Normalize Amplitude 2ºH SON','e) Phase of the semi-diurnal peak 2ºH SON','f) Phase of the semi-diurnal peak 2ºH SON']

# A variável "ppmean" têm unidades de mm/0.5hour, já que é a média dos 48 registos (dt = 0.5hour) no dia
# Essa variável "ppmean" vai ser transformada com unidades de mm/hour na média de 24 horas com 24 registros
#ds['ppmean'] = ds['ppmean'] * 2

print("4. Terminou de ler os datasets")
#------------------------------------------------------------------------------------------------------
# Criando un class para calcular os mid_points
print("5. Criando um class para calcular os mid points")
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
print("6. Terminou de criar o class dos mid points")
#-------------------------------------------------------------------------------------------------------------
# Estabelecendo as características do gráfico
print("7. Criando figura para os plots")
fig = plt.figure(figsize = (15,10), dpi = 100) 
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
print("8. Terminou de estabelecer os parâmetros para as figuras")

print("9. Fazendo o loop para gerar as figuras dos parâmetros diurnos")
for i in range(1,7,1):
    # Fazendo os subplots com suas projeções
    axx[i-1] = fig.add_subplot(2,3,i, projection = ccrs.PlateCarree())
    #axx[i-1].set_extent([lon_min, lon_max, lat_min, lat_max], ccrs.PlateCarree())
    # Agregando linhas de costa
    axx[i-1].coastlines('50m')
    # Formatando a latitude e longitude
    axx[i-1].xaxis.set_major_formatter(LongitudeFormatter())
    axx[i-1].yaxis.set_major_formatter(LatitudeFormatter())
    # Agregando linhas da grade
    gl = axx[i-1].gridlines(draw_labels = True)
    # Removendo os labels da grade do lado superior
    gl.top_labels = False
    # Removendo os labels da grade do lado direito
    gl.right_labels = False
    # Estabelendo o size dos labels no eixo X
    gl.xlabel_style = {'size': 12}
    # Estabelecendo o size dos labels no eixo Y
    gl.ylabel_style = {'size': 12}
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
    norm = MidpointNormalize(vmin = ds[f'{vars[i-1]}'].min(), vmax = ds[f'{vars[i-1]}'].max(), midpoint = mid_point[i-1])
    # Fazendo o plotagem para cada panel

    if i == 3:  # Editando a paleta de cores para a Fase do 1º Harmônico (norm = norm1)
        ds[f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm1,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})
        # Sinais de taxa de precipitação fraca < 0.01 mm/h
        axx[i-1].contourf(ds['lon'], ds['lat'], ds['ppmean'] <= 0.01, colors = 'none', hatches = ['XXXX'], levels=[0.6,1.5])
    else:       # Editando a paleta de cores considerando o ponto médio (norm = norm)
        ds[f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})
        # Sinais de taxa de precipitação fraca < 0.01 mm/h
        axx[i-1].contourf(ds['lon'], ds['lat'], ds['ppmean'] <= 0.01, colors = 'none', hatches = ['XXXX'], levels=[0.6,1.5])

    # Topografia
    colorb=np.arange(1500,1550,50)
    cb = axx[i-1].contour(ds_topo_ba.lon, ds_topo_ba.lat, ds_topo_ba['z'], levels = colorb, colors = ['brown'], linewidths=0.5)

    # Agrendo title aos paneis de cada subplot
    axx[i-1].set_title(f'{title[i-1]}', size = 12, fontweight = 'bold', fontfamily = 'sans')
    # Ajustando os subplots
    plt.subplots_adjust(hspace=0.15, wspace=0.05, left=0.125, bottom=0.1, right=0.9, top=0.9)

print("10. Figuras dos parâmetros diurnos")
plt.show()

print("11. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/OUTPUTS_PARAMETERS_DIURNAL_AS/Parameters_diurnal_cycle_' + f'{periodo}_AS.png', format='png', dpi = 100)

print("12. Finalizou de executar o código")
