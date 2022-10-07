"""
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# MSc. Student at Institute of Astronomy, Geophisycs and Atmospheric Sciences at University of São Paulo
# File: mean_seasonal_atmospheric_circulation_200hPa.py 
#
# Descriptiopn:
# Esse script faz os gráficos da circulação atmosférica sazonal média 
# no nível de 200 hPa (vetores), incluindo a topografia dos Andes (acima do nível de 1500 msnm),
# o contorno de 1500 msnm e o contorno (shapefile) da Bacia Amazônica para as estações do ano
# DJF, MAM, JJA e SON no período de 2001 - 2020. 
#
"""
#
# -------------------------------------------------------------------------------------------------------------------
#
# Livrarias de leitura e processamento de dados
print('Executar o código')

print('1. Importar os pacotes')
import xarray as xr
import numpy as np

# Importar pacotes de geração de mapas
import cartopy.crs as ccrs # Pacote para mapas (sistema de referência cooordenado)
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

# Livrarias para fazer edição das figuras
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
print('2. Terminou de importar os pacotes')
#
# -------------------------------------------------------------------------------------------------------------------
#
# Ler o dataset de circulação para o período de 2001 - 2020
# u: componente zonal
# v: componente meridional
# Resolução: 0.25º x 0.25º
# Source: ERA5 (Hersbach et al., 2020)
# Período: 2001 - 2020
# Link: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels-monthly-means?tab=form
print('3. Ler o dataset de circulação')
ds = xr.open_dataset('/home/ronaldrn/ronald/mestrado/NETCDF_ATMOSPHERIC_CIRCULATION/circulation_mean_season_AS.nc')

# Calcular a média sazonal (DJF, MAM, JJA, SON) da circulação atmosférica em níveis baixos (850 hPa)
print('4. Calcular a média sazonal para todo o período')   
ds_mean = ds.groupby('time.season').mean(dim=['time'])

# Ler o dataset da topografia 
# dado de topografia baixado do seguinte link: 
# https://topex.ucsd.edu/WWW_html/mar_topo.html
# https://topex.ucsd.edu/pub/global_topo_1min/
# Resolução espacial de aproximadamente: ~2 kilometer
# Resolução em Z: ~150 meters
print('5. Ler o dado de topografia')
ds_topo = xr.open_dataset('/home/ronaldrn/ronald/mestrado/topography/topo_23.1.nc')
# Fazendo um slice para a Área da Bacia Amazônica
print('6. Fazer um slice do dataset de topografia centrado na Amazônia')
ds_topo_ba = ds_topo.sel(lat=slice(-25, 10), lon=slice(-85, -45))
#
# -------------------------------------------------------------------------------------------------------------------
#
# Fazer a Figura com os gráficos sazonais
print('7. Criando a figura para os plots')
fig, axes = plt.subplots(2,2, figsize=(10,14), constrained_layout=True,subplot_kw = {'projection': ccrs.PlateCarree()})

print('8. Configurando o colorbar')
# Configurando a paleta de cores (colorbar) do 'terrain' com novos intervalos para o dataset de topografia
new_terrain = cm.get_cmap('terrain', 59)
# Estabelcendo os límites do colorbar
boundaries = np.arange(-1400,4550,100)
# Estabelcer os novos límites do colorbar
norm1 = matplotlib.colors.BoundaryNorm(boundaries, new_terrain.N, clip=True)

# Colorbar para o campo de divergência
bounds = np.linspace(-12, 12, 12)
norm = matplotlib.colors.BoundaryNorm(boundaries=bounds, ncolors=256)

print('9. Criando listas para os plots dentro do loop')
# Criando uma lista com os objetos para cada ṕlot
ax = [axes[0,0], axes[0,1], axes[1,0], axes[1,1]]
# Criando uma lista com os títulos dos plots dentro do loop
title = ['a) Circulação atmosférica a 200 hPa\nPeríodo:DJF [2001-2020]', 'c) Circulação atmosférica a 200 hPa\nPeríodo:JJA [2001-2020]',\
        'b) Circulação atmosférica a 200 hPa\nPeríodo:MAM [2001-2020]', 'd) Circulação atmosférica a 200 hPa\nPeríodo:SON [2001-2020]']

# -------------------------------------------------------------------------------------------------------------------------
print('10. Executar o loop para gerar plots')
for i in range(1,5,1):
    # Extensão do límites dos plots (mapas)
    ax[i-1].set_extent([-85, -45, 15, -25], ccrs.PlateCarree())
    # Configurar linhas de grade para os plots
    gl = ax[i-1].gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
    # Removendo os labels da grade do lado superior
    gl.top_labels = False
    # Removendo os labels da grade do lado direito
    gl.right_labels = False
    # Estabelendo o size dos labels no eixo X
    gl.xlabel_style = {'size': 14}
    # Estabelecendo o size dos labels no eixo Y
    gl.ylabel_style = {'size': 14}
    #Formatndo os labels dos ticks como latitude e longitude (°)
    gl.yformatter = LATITUDE_FORMATTER
    gl.xformatter = LONGITUDE_FORMATTER

    # Agregar linhas de costa no mapa
    ax[i-1].add_feature(cfeature.COASTLINE)
    # Agregar os límites entre paises
    ax[i-1].add_feature(cfeature.BORDERS, edgecolor = '0.25')
    # Agregar os estado do Brasil
    states_provinces = cfeature.NaturalEarthFeature(
        category = 'cultural',
        name = 'admin_1_states_provinces_lines',
        scale = '50m',
        facecolor = 'none')
    ax[i-1].add_feature(states_provinces, edgecolor = 'gray')

    # Agregar o file do contornbo da Bacia Amazônica
    fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
    # Ler o shapefile da Bacia Amazônica
    adm1_shapes = list(shpreader.Reader(fname).geometries())
    # Agregando o shapefile ao plot
    ax[i-1].add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='green', facecolor='none', alpha=1, linewidth = 2)
    # Agregar os títulos dos plots
    ax[i-1].set_title(f'{title[i-1]}', y=1.0, size=14, fontweight='bold', fontfamily='sans')

    # Agregar a topografia acima de 1500 msnm no formato sombrado (shaded)
    #im = ax[i-1].contourf(ds_topo_ba.lon, ds_topo_ba.lat, ds_topo_ba.z, cmap = "terrain", 
    #                    levels = np.arange(1500, ds_topo_ba.z.max(), 100), vmin=-2200)

    # Agregando o contorno de 1500 m
    colorb=np.arange(1500,1550,50)
    cb = ax[i-1].contour(ds_topo_ba.lon, ds_topo_ba.lat, ds_topo_ba['z'], levels = colorb, colors = ['brown'], linewidths=0.75)

    # Agregar o campo de divergência 
    div = ax[i-1].contourf(ds_mean.longitude, ds_mean.latitude, (ds_mean['d']*10**6).isel(season=i-1, level = 0), norm=norm, cmap = "RdBu_r",\
        transform = ccrs.PlateCarree(), levels=np.arange(-9,10,2), extend='both')

    # Agregar os dados de vento horizontal no formato de linhas de corrente
    strm = ax[i-1].streamplot(ds_mean.longitude, ds_mean.latitude, ds_mean['u'].isel(season=i-1, level=0).values,\
        ds_mean['v'].isel(season=i-1, level=0).values, color='black', transform = ccrs.PlateCarree(), density=[2,2])

print('11. Terminou de executar o loop')
#
# ------------------------------------------------------------------------------------------------------------------------------
#
print('12. Configurar o colorbar da divergência')
# Adicionando a barra de cor
cbar = fig.colorbar(div, ax=axes[:,1], ticks=np.arange(-9, 10, 2), shrink=0.5, pad=0.05, fraction=.1)
# Legenda da colorbar 
cbar.set_label('Divergência * $10^{-6}s^{-1}$', size=14)
#cbar.axes.tick_params(labelsize=13) # tamanho da legenda dos ticks

# Menos espaço entre os plots
fig.tight_layout

plt.show()

print("13. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_CIRCULATION/mean_sazonal_circulation_200hPa.png', format='png', dpi = 300)

print('14. Terminou de executar o código')
