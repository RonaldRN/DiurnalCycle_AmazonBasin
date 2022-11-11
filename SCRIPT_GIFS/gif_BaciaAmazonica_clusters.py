'''
#
# Author: Ronald Guiuseppi Ramírez Nina
# Estudante de Mestrado no Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Paulo
# 
# File: gif_BaciaAmazonica_clusters.py
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
    # Setor NE:Posições     00 - 05
    # Setor E: Posições     06 - 11
    # Setor N: Posições     12 - 17
    # Setor C: Posições     18 - 23
    # Setor S: Posições     24 - 29
    # Setor NW:Posições     30 - 35
    # Setor SW:Posições     36 - 41
    ds = salem.open_xr_dataset(file_DJF)
    lat = [-1.956206,-0.094217,-1,-1,-0.8597,0,-4,-5.40,-3.80,-2.5,-5,-5,0.368947,0.75,0.25,4.279977,1.22,3,-5,-8.447258,-9.5,-5,-2,-3.20,\
        -19.08,-14,-13,-20,-15,-17.45,-3.3,-1.32,-3,1,-6.48,-5,-13,-16.5,-12,-18.4,-13.77,-16.1]
    lon = [-53.466879,-50.729194,-55,-54,-50.40,-57,-53,-53,-54.53,-55.54,-51.38393,-58,-67.853762,-62,-67.13,-60.571129,-65.58,-63,-70,-57,-66.739,-65,-63,-60,\
        -63.69,-64,-57,-64,-60,-64,-72,-76.28,-74.15,-72,-77.78,-78,-70.663321,-65.77,-67,-65.77,-73.81,-66.73]
    cluster = [1,2,3,4,5,6,1,2,3,6,6,2,1,2,3,4,5,6,1,2,2,3,4,2,1,2,3,3,4,6,1,2,3,4,5,6,1,1,2,4,5,6]

elif periodo == 'MAM':
    # Setor NE:Posições     00 - 05
    # Setor E: Posições     06 - 11
    # Setor N: Posições     12 - 17
    # Setor C: Posições     18 - 23
    # Setor S: Posições     24 - 29
    # Setor NW:Posições     30 - 35
    # Setor SW:Posições     36 - 41
    ds = salem.open_xr_dataset(file_MAM)
    lat = [0,-0.55,0.9,0,-1,-1.18,-5,-5,-4,-5.44,-2.1,-3,0.71,2.26,4.437964,0.5,3,1.25,-5,-3.41,-2.4,-3.26,-2.41,-3,\
        -10.5,-10,-13,-10.72,-19,-13,-3,-3,-1.23,-2,-4.52,-7,-13,-16.8,-11.45,-12,-12,-14]
    lon = [-55,-57.5,-53.81,-51,-54,-56.81,-55,-53,-57.5,-50.99,-52.16,-58.65,-68.39,-67.27,-60.539219,-63.9,-63,-65.82,-65,-69,-62.67,-58.7,-67.85,-60,\
        -55.36,-57.2,-54,-58.26,-64,-52.16,-75,-72,-78.56,-76.77,-78.17,-78.17,-70.663321,-65.33,-75,-67,-73,-74]
    cluster = [1,2,3,4,1,2,1,2,4,5,1,4,1,2,3,4,5,3,1,2,3,4,4,4,1,2,3,4,5,6,1,2,3,4,5,6,2,2,3,3,5,6]

elif periodo == 'JJA':
    # Setor NE:Posições     00 - 05
    # Setor E: Posições     06 - 11
    # Setor N: Posições     12 - 17
    # Setor C: Posições     18 - 23
    # Setor S: Posições     24 - 29
    # Setor NW:Posições     30 - 35
    # Setor SW:Posições     36 - 41
    # Cluster 0: É uma região com sinais fracas de precipitação < 0.01 mm/h
    ds = salem.open_xr_dataset(file_JJA)
    lat = [-1.28,2,-1.67,0.22,0.8,-1.25,-5,-2.12,-5,-5.54,-3.38,-3,2.4,3.18,1.34,2.887,0.71,4.49,-2.537,-2.5,-2.63,-2.83,-3,-4,\
        -13,-13.29,-17,-18,-12,-20,-6.3,0,-6,-7,-3.5,0.37,-13,-16.8,-12.85,-11.4,-15,-14]
    lon = [-55.45,-55,-57.34,-50.85,-57.5,-55.40,-51,-55.598,-59,-53.81,-58.75,-52,-67.61,-61.07,-65.58,-63.45,-65,-59.81,-59.52,-67,-62,-58.17,-69,-64.32,\
        -60,-64.51,-61,-63,-56,-64,-78.07,-77,-73.5,-76,-72,-77.54,-70.663321,-65.63,-74.34,-75,-66,-73.67]
    cluster = [1,3,4,5,6,1,1,2,3,4,5,6,2,2,3,4,5,6,1,2,3,4,5,4,1,3,4,6,0,0,1,2,3,4,5,6,6,6,1,3,4,0]

elif periodo == 'SON':
    # Setor NE:Posições     00 - 05
    # Setor E: Posições     06 - 11
    # Setor N: Posições     12 - 17
    # Setor C: Posições     18 - 23
    # Setor S: Posições     24 - 29
    # Setor NW:Posições     30 - 35
    # Setor SW:Posições     36 - 41
    ds = salem.open_xr_dataset(file_SON)
    lat = [-1.37,1,0,-0.5,0.5,0.93,-5.83,-4,-5.85,-5,-13,-5,5,3.52,1,0.27,2.31,2,-2.34,-2.5,-5,-2.73,-2.73,-4,\
        -13,-18.2,-13,-20,-16.75,-17,-6.43,-5.27,-3,1,-3.36,-3.55,-13,-16.8,-15,-13.87,-10.55,-18.5]
    lon = [-53,-55,-51,-56.4,-57.7,-58.21,-53,-52,-56.91,-55,-52.74,-51,-60,-62.38,-69.36,-66.55,-67.61,-63,-61.85,-69,-65,-67.32,-57.78,-66,\
        -60,-63,-56,-64.17,-64.66,-62,-77.93,-78.61,-73.3,-73,-72,-77.25,-70,-65.2,-68.68,-68.63,-66.3,-66]
    cluster = [1,2,5,1,2,4,1,2,3,4,4,7,1,2,3,4,6,7,1,3,4,6,7,4,1,2,4,5,6,7,1,2,3,4,6,7,6,6,1,2,4,5]

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
    
    for j in np.arange(0,42,1):
        ax.scatter(lon[j], lat[j], s=50, color= "black", marker=r'${0}$'.format(0+cluster[j]), edgecolor="black", alpha=0.8, zorder=10)

    ax.set_title(f'{periodo}' + '[2001-2020] - ' + 'hora: ' + hour[i] + 'UTC - ', fontsize=18, y=1.02)

    fig.tight_layout

    fig.savefig('/home/ronaldrn/ronald/mestrado/gif_horario/GIF_BA/' + f'{periodo}_BA_ciclo_diurno_' + f'{i}_clusters.png', format='png', dpi = 100)

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
    filenames_DJF = [output + "DJF_BA_ciclo_diurno_"+str(i)+"_clusters.png" for i in range(48)]
    filenames_MAM = [output + "MAM_BA_ciclo_diurno_"+str(i)+"_clusters.png" for i in range(48)]
    filenames_JJA = [output + "JJA_BA_ciclo_diurno_"+str(i)+"_clusters.png" for i in range(48)]
    filenames_SON = [output + "SON_BA_ciclo_diurno_"+str(i)+"_clusters.png" for i in range(48)]

    filenames = filenames_DJF + filenames_MAM + filenames_JJA + filenames_SON

    with imageio.get_writer('/home/ronaldrn/ronald/mestrado/gif_horario/GIF_BA/Amazon_basin_clusters_gif.gif', mode='I', duration = 0.2) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    print("8. Removendo as figuras e só salvando a GIF")
    # Remove files
    for filename in set(filenames):
        os.remove(filename)

print("9. Execução do código finalizada")