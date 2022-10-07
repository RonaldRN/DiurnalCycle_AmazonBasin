"""
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# MSc. Student at Institute of Astronomy, Geophisycs and Atmospheric Sciences at University of São Paulo
#
# File: DiurnalCycle_HarmonicParam_seasonBA.py
# Esse script faz os gráficos dos parâmetros da Análise harmônica: Taxa de precipitação média,
# amplitude normalizada (1ºH e 2ºH), fase (1ºH e 2ºH), e diferença relativa entre a amplitude do 1ºH e 2ºH
#  para a Bacia Amazônica por estação do ano (DJF, MAM, JJA e SON).
#
"""

print("EXECUTANDO O CÓDIGO")

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
# Path of the file
file_DJF = '/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_DJF.nc'
file_MAM = '/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_MAM.nc'
file_JJA = '/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_JJA.nc'
file_SON = '/home/ronaldrn/ronald/mestrado/NETCDF_MASK_BA/BA_mask_SON.nc'
# Abrindo o arquivo NetCDF
print("3. Ler datasets")
ds1 = xr.open_dataset(file_DJF)     # File do dataset de DJF
ds2 = xr.open_dataset(file_MAM)     # File do dataset de MAM
ds3 = xr.open_dataset(file_JJA)     # File do dataset de JJA
ds4 = xr.open_dataset(file_SON)     # File do dataset de SON
print("4. Terminou de ler os datasets")

# Criando a variável das Diferença Relativa entre o 1ºH e 2ºH
print('5. Criando a variável de Diferença Relativa entre o 1ºH e o 2ºH')
ds1['dif_rel'] = ((ds1['C1_24h'] - ds1['C2_24h']) / (ds1['C1_24h'])) * 100
ds2['dif_rel'] = ((ds2['C1_24h'] - ds2['C2_24h']) / (ds2['C1_24h'])) * 100
ds3['dif_rel'] = ((ds3['C1_24h'] - ds3['C2_24h']) / (ds3['C1_24h'])) * 100
ds4['dif_rel'] = ((ds4['C1_24h'] - ds4['C2_24h']) / (ds4['C1_24h'])) * 100

print('6. Ler o dado de topografia')
ds_topo = xr.open_dataset('/home/ronaldrn/ronald/mestrado/topography/topo_23.1.nc')
# Fazendo um slice para a Área da Bacia Amazônica
print('7. Fazer um slice do dataset de topografia centrado na Amazônia')
ds_topo_ba = ds_topo.sel(lat=slice(-25, 10), lon=slice(-85, -45))

# ------------------------------------------------------------------------------------------------------------
#
# Agregar una imagen satelital de fondo
# Importando os para estabelecer o diretório de trabalho para a imagem de fondo
print("8. Importan uma imagem satelital de fondo")
print("9. Importando o pacote os")
import os as os
# Estabelcer o diretório para a imagem de fondo
print("10. Path do diretório de trabalho atual")
current_directory = os.getcwd()
# Configurando um environment variable
print("11. Configurando um environment variable")
os.environ["CARTOPY_USER_BACKGROUNDS"] = os.path.join(current_directory,'CARTOPY_IMGS')
os.getenv('CARTOPY_USER_BACKGROUNDS')
# Extenção da imagem
print("12. Extenção da imagem")
lat_min = -25 # Latitude mínima do plot
lat_max = 10  # LAtitude máxima do plot
lon_min = -82 # Longitude mínima do plot
lon_max = -48 # Longitude máxima do plot
extent = [lon_min, lon_max, lat_min, lat_max]

#------------------------------------------------------------------------------------------------------
# Criando un class para calcular os mid_points
print("13. Criando um class para calcular os mid points")
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
print("14. Terminou de criar o class dos mid points")
#-------------------------------------------------------------------------------------------------------------
# Estabelecendo as características do gráfico
print("15. Criando figura para os plots")
fig = plt.figure(figsize = (12,10), dpi = 100) 
#plt.title('Parâmetros do Análise harmônico do Ciclo Diurno para o período DJF', size = 20)
plt.axis = ('off')
plt.subplots_adjust(wspace=0.3,hspace=0.0001)

# Para eliminar marco da figura completa
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False) 
for pos in ['right', 'top', 'bottom', 'left']:
     plt.gca().spines[pos].set_visible(False)
#-------------------------------------------------------------------------------------------------------
# Datasets
ds = [ds1,ds2,ds3,ds4]
# ------------------------------------------------------------------------------------------------------
print("--------------------------------------------------------------------")
print('                                                                    ')
print("DIGITAR O CÓDIGO DA VARIÁVEL DE INTERESSE:")
print('                                                                    ')
print("1: Taxa de Precipitação média")
print("2: Amplitude Normalizada do 1º Harmônico")
print("3: Fase em Local Solar Time do 1º Harmônico")
print("4: Amplitude Normalizada do 2º Harmônico")
print("5: Fase em Local Solar Time do 2º Harmônico - 1º Máximo")
print("6: Fase em Local Solar Time do 2º Harmônico - 2º Máximo")
print("7: Diferença Relativa entre o 1ºH e o 2ºH")
print('                                                                    ')
variavel = input("Digite o código da variável da sua interesse: ")
print('                                                                    ')

if variavel == '1':     # Taxa de precipitação média
    # Selecionando a variável para cada estação dos datasets
    vars = ['ppmean','ppmean','ppmean','ppmean']
    # Titulo para cada estação
    title = ['a) Mean Precipitation Rate (mm/hour)\n[DJF 2001-2020]','b) Mean Precipitation Rate (mm/hour)\n[MAM 2001-2020]',\
        'c) Mean Precipitation Rate (mm/hour)\n[JJA 2001-2020]', 'd) Mean Precipitation Rate (mm/hour)\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['BrBG','BrBG','BrBG','BrBG']
    # Nome do label do colobar
    labels = ['Mean Precipitation Rate (mm/hour)','Mean Precipitation Rate (mm/hour)',\
        'Mean Precipitation Rate (mm/hour)','Mean Precipitation Rate (mm/hour)']
    # Ponto médio do colorbar
    mid_point = [0.275, 0.275, 0.275, 0.275]

elif variavel == '2':   # Amplitude Normalizada do 1ºH
    # Selecionando variáveis para cada estação dos datasets
    vars = ['C1_24h','C1_24h','C1_24h','C1_24h']
    # Titulo para cada estação
    title = ['a) Normalized Amplitude 1ºH\n[DJF 2001-2020]','b) Normalized Amplitude 1ºH\n[MAM 2001-2020]',\
        'c) Normalized Amplitude 1ºH\n[JJA 2001-2020]','d) Normalized Amplitude 1ºH\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['PuOr', 'PuOr', 'PuOr', 'PuOr']
    # Nome do label do colorbar
    labels = ['Ratio of Amp. to Mean of 1ºH','Ratio of Amp. to Mean of 1ºH','Ratio of Amp. to Mean of 1ºH','Ratio of Amp. to Mean of 1ºH']
    # Ponto médio do colorbar
    mid_point = [0.5, 0.5, 0.5, 0.5]

elif variavel == '3':   # Fase LST do 1ºH
    # Selecionando variáveis para cada estação
    vars = ['F1_LST','F1_LST','F1_LST','F1_LST']
    # Titulo para cada estação
    title = ['a) Phase of the diurnal peak 1ºH\n[DJF 2001-2020]','b) Phase of the diurnal peak 1ºH\n[MAM 2001-2020]',\
        'c) Phase of the diurnal peak 1ºH\n[JJA 2001-2020]','d) Phase of the diurnal peak 1ºH\n[SON 2001-2020]']
    # Nome do colorbar
    labels = ['Local Solar Time do Max. [hour]','Local Solar Time do Max. [hour]','Local Solar Time do Max. [hour]','Local Solar Time do Max. [hour]']

elif variavel == '4':   # Amplitude Normalizada do 2ºH
    # Selecionando variáveis para cada estação dos datasets
    vars = ['C2_24h','C2_24h','C2_24h','C2_24h']
    # Titulo para cada estação
    title = ['a) Normalized Amplitude 2ºH\n[DJF 2001-2020]','b) Normalized Amplitude 2ºH\n[MAM 2001-2020]',\
        'c) Normalized Amplitude 2ºH\n[JJA 2001-2020]','d) Normalized Amplitude 2ºH\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['plasma', 'plasma', 'plasma', 'plasma']
    # Nome do label do colorbar
    labels = ['Ratio of Amp. to Mean of 2ºH','Ratio of Amp. to Mean of 2ºH','Ratio of Amp. to Mean of 2ºH','Ratio of Amp. to Mean of 2ºH']
    # Ponto médio do colorbar
    mid_point = [0.5, 0.5, 0.5, 0.5]

elif variavel == '5':   # Fase LST do 2ºH
    # Selecionando variáveis de cada colorbar
    vars = ['F2_LST','F2_LST','F2_LST','F2_LST']
    # Titulo para cada estação
    title = ['a) Phase of the semi-diurnal peak 2ºH\n[DJF 2001-2020]','b) Phase of the semi-diurnal peak 2ºH\n[MAM 2001-2020]',\
        'c) Phase of the semi-diurnal peak 2ºH\n[JJA 2001-2020]','d) Phase of the semi-diurnal peak 2ºH\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['twilight_shifted','twilight_shifted','twilight_shifted','twilight_shifted']
    # Nome do colorbar
    labels = ['2ºH Local Solar Time do Max. [hour]','2ºH Local Solar Time do Max. [hour]',\
        '2ºH Local Solar Time do Max. [hour]','2ºH Local Solar Time do Max. [hour]']
    # Ponto médio do colorbar
    mid_point = [6, 6, 6, 6]

elif variavel == '6':   # Fase do segundo máximo LST do 2ºH
    # Selecionando variáveis de cada colorbar
    vars = ['F2_12h_LST','F2_12h_LST','F2_12h_LST','F2_12h_LST']
    # Titulo para cada estação
    title = ['a) Phase of the semi-diurnal peak 2ºH\n[DJF 2001-2020]','b) Phase of the semi-diurnal peak 2ºH\n[MAM 2001-2020]',\
        'c) Phase of the semi-diurnal peak 2ºH\n[JJA 2001-2020]','d) Phase of the semi-diurnal peak 2ºH\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['RdGy','RdGy','RdGy','RdGy']
    # Nome do colorbar
    labels = ['2ºH Local Solar Time do Max. [hour]','2ºH Local Solar Time do Max. [hour]',\
        '2ºH Local Solar Time do Max. [hour]','2ºH Local Solar Time do Max. [hour]']
    # Ponto médio do colorbar
    mid_point = [18, 18, 18, 18]

elif variavel == '7':   # Diferença Relativa entre o 1ºH e o 2ºH
    # Selecionando variáveis de cada colorbar
    vars = ['dif_rel','dif_rel','dif_rel','dif_rel']
    # Titulo para cada estação
    title = ['a) Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)' + '\n[DJF 2001-2020]',\
        'b) Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)' + '\n[MAM 2001-2020]',\
        'c) Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)' + '\n[JJA 2001-2020]',\
        'd) Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)' + '\n[SON 2001-2020]']
    # Cor para o plot da variável
    colors_map = ['PuOr', 'PuOr', 'PuOr', 'PuOr']
    # Nome do colorbar
    labels = ['Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)',\
        'Diferença Relativa da Ampl. 1ºH e 2ºH ' + u'(C\u2081-\u2082)',\
        'Diferença Relativa da Ampl. 1ºH e 2ºH DJF ' + u'(C\u2081-\u2082)',\
        'Diferença Relativa da Ampl. 1ºH e 2ºH DJF ' + u'(C\u2081-\u2082)']
    # Ponto médio do colorbar
    mid_point = [0, 0, 0, 0]

# Nome dos subplots
axx = ['ax1','ax2','ax3','ax4']

# Nova paleta de cores para a fase do 1º harmônico
new_hsv = cm.get_cmap('hsv', 24)
boundaries = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
norm1 = matplotlib.colors.BoundaryNorm(boundaries, new_hsv.N, clip=True)
print("16. Terminou de estabelecer os parâmetros para as figuras")

print("17. Fazendo o loop para gerar as figuras dos parâmetros diurnos")
for i in range(1,5,1):

    #axx[i-1].set_extent([lon_min, lon_max, lat_min, lat_max], ccrs.PlateCarree())

    # Fazendo os subplots com suas projeções
    axx[i-1] = fig.add_subplot(2,2,i, projection = ccrs.PlateCarree())
    axx[i-1].set_extent([lon_min, lon_max, lat_min, lat_max], ccrs.PlateCarree())
    # Agregando linhas de costa
    axx[i-1].coastlines('50m')
    # Formatando a latitude e longitude
    axx[i-1].xaxis.set_major_formatter(LongitudeFormatter())
    axx[i-1].yaxis.set_major_formatter(LatitudeFormatter())
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

    # Fazendo o plotagem para cada panel

    # Editando a paleta de cores para a Fase do 1º Harmônico (norm = norm1)
    if vars[i-1] == 'F1_LST':
        ds[i-1][f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = new_hsv, norm = norm1,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})

    elif vars[i-1] == 'dif_rel':
    # Definindo os valores máximos, mínimos e o mid_point das paletas de cores
        norm = MidpointNormalize(vmin = -80, vmax = 80, midpoint = mid_point[i-1])
    # Editando a paleta de cores considerando o ponto médio (norm = norm) para as outras variáveis
        ds[i-1][f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})

    else:
    # Definindo os valores máximos, mínimos e o mid_point das paletas de cores
        norm = MidpointNormalize(vmin = ds[i-1][f'{vars[i-1]}'].min(), vmax = ds[i-1][f'{vars[i-1]}'].max(), midpoint = mid_point[i-1])
    # Editando a paleta de cores considerando o ponto médio (norm = norm) para as outras variáveis
        ds[i-1][f'{vars[i-1]}'].plot(ax = axx[i-1], x='lon', y='lat', cmap = f'{colors_map[i-1]}', norm = norm,\
            transform = ccrs.PlateCarree(), cbar_kwargs = {'label':f'{labels[i-1]}','shrink':0.60})

    axx[i-1].contourf(ds[i-1]['lon'], ds[i-1]['lat'], ds[i-1]['ppmean'] <= 0.01, colors = 'none', hatches = ['XXX'], levels=[0.6,1.5])
    
    # Topografia
    colorb=np.arange(1500,1550,50)
    cb = axx[i-1].contour(ds_topo_ba.lon, ds_topo_ba.lat, ds_topo_ba['z'], levels = colorb, colors = ['brown'], linewidths=0.5)

    # Agrendo title aos paneis de cada subplot
    axx[i-1].set_title(f'{title[i-1]}', size = 14, fontweight = 'bold', fontfamily = 'sans')
    # Ajustar os subplots
    plt.subplots_adjust(hspace=0.15, wspace=0.05, left=0.125, bottom=0.1, right=0.9, top=0.9)

fig.tight_layout()

print("18. Figuras dos parâmetros diurnos")
plt.show()

print("19. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/OUTPUTS_PARAMETERS_DIURNAL_BA/' + f'{vars[0]}_diurnal_cycle_BA.png', format='png', dpi = 100)

print("20. Terminou de executar o código")