'''
#
# Author: Ronald Guiuseppi Ramírez Nina
# Estudante de Mestrado no Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Paulo
# 
# File: gif_BaciaAmazonica.py
# Este file .py faz um gif da taxa de precipitação média horária a cada paso de tempo de 0.5h
# para toda a Bacia Amazônica e para os períodos de DJF, MAM, JJA e SON 
#
'''
###########################################################################################

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

# Nome do arquivo
file_DJF = '/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_DJF.nc'
file_MAM = '/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_MAM.nc'
file_JJA = '/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_JJA.nc'
file_SON = '/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_SON.nc'

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
print("3. Ler datasets")

# Abrindo o arquivo NetCDF
if periodo == 'DJF':
    ds = salem.open_xr_dataset(file_DJF)
elif periodo == 'MAM':
    ds = salem.open_xr_dataset(file_MAM)
elif periodo == 'JJA':
    ds = salem.open_xr_dataset(file_JJA)
elif periodo == 'SON':
    ds = salem.open_xr_dataset(file_SON)

print("4. Ler o dhapefile da Bacia Amazônica")
# Abrindo o shapefile da Bacia amazônica
shp = salem.read_shapefile('/home/ronaldrn/ronald/mestrado/Amazonia_internacional_SIRGAS_2000/amazlm_poly_1608.shp')
shp_ba = shp.loc[shp.index == 3]

print("5. Fazer um clip sobre os dados do IMERG com shapefila da BA")
# Fazendo o corte da BA com o shapefile
dsr = ds.salem.roi(shape = shp_ba).sel(lat=slice(-25, 10), lon=slice(-82, -48))

dsr['precipitationCal'] = dsr['precipitationCal']

# Lista dos passos de tempo (0.5h) dos dados do IMERG
hour = ['00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30','06:00',\
    '06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00',\
        '13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00',\
            '20:30','21:00','21:30','22:00','22:30','23:00','23:30']

# Intervalos da paleta de cores
levels = np.arange(0,0.82,0.02)

print("6. Fazendo os plots .png para cada passo de tempo")
for i in np.arange(0,48,1):

    fig = plt.figure(figsize=(10,7))

    ax = fig.add_subplot(1,1,1, projection = ccrs.PlateCarree())

    import os as os
    current_directory = os.getcwd()
    os.environ["CARTOPY_USER_BACKGROUNDS"] = os.path.join(current_directory,'CARTOPY_IMGS')
    os.getenv('CARTOPY_USER_BACKGROUNDS')
    extent = [-82,-48, -25, 10]
    ax.background_img(name='BM_NASA', resolution='low', extent=extent)
    # Agregando linhas da grade
    gl = ax.gridlines(draw_labels = True)
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
    ax.add_feature(rivers_50m, facecolor = 'None', edgecolor = 'b', linewidth = 1)
    # Agregando os paises
    ax.add_feature(cfeature.BORDERS, edgecolor='0.25')
    # Agregando Estados
    states_provinces = cfeature.NaturalEarthFeature(
        category = 'cultural',
        name = 'admin_1_states_provinces_lines',
        scale = '50m',
        facecolor = 'none')
    ax.add_feature(states_provinces, edgecolor = '0.25')
    # Agregando o shapefile da Bacia Amazônica
    fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
    adm1_shapes = list(shpreader.Reader(fname).geometries())
    ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='yellow', facecolor='none', alpha=1, linewidth = 2)

    dsr['precipitationCal'][i].plot(x='lon', y='lat',cmap='jet',vmin = 0.1, vmax = 0.8, levels = levels, \
        cbar_kwargs = {'label':'Taxa de precipitação [mm/h]'})
    ax.set_title(f'{periodo}' + '[2001-2020] - ' + 'hora: ' + hour[i] + 'UTC - ', fontsize=18, y=1.02)

    fig.tight_layout

    fig.savefig('/home/ronaldrn/ronald/mestrado/gif_horario/GIF_BA/' + f'{periodo}_BA_ciclo_diurno_' + f'{i}.png', format='png', dpi = 100)

    #plt.show()

print("7. Criando o Gif")
if periodo == 'SON':
    # Fazendo o Gif
    import imageio.v2 as imageio
    import os
    import matplotlib.pyplot as plt

    # animation
    # ---------
    filenames = []
    # plot the line chart

    output = "/home/ronaldrn/ronald/mestrado/gif_horario/GIF_BA/"
    filenames_DJF = [output + "DJF_BA_ciclo_diurno_"+str(i)+".png" for i in range(48)]
    filenames_MAM = [output + "MAM_BA_ciclo_diurno_"+str(i)+".png" for i in range(48)]
    filenames_JJA = [output + "JJA_BA_ciclo_diurno_"+str(i)+".png" for i in range(48)]
    filenames_SON = [output + "SON_BA_ciclo_diurno_"+str(i)+".png" for i in range(48)]

    filenames = filenames_DJF + filenames_MAM + filenames_JJA + filenames_SON

    with imageio.get_writer('/home/ronaldrn/ronald/mestrado/gif_horario/GIF_BA/Amazon_basin_gif.gif', mode='I', duration = 0.2) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    print("8. Removendo as figuras e só salvando a GIF")
    # Remove files
    for filename in set(filenames):
        os.remove(filename)

print("9. Execução do código finalizada")