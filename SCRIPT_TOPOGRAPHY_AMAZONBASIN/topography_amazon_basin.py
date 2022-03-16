'''
#
# Author: Ronald Guiuseppi Ramírez Nina
# Estudante de Mestrado no Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Paulo
# 
# File: topografy_amazon_basin.py
# Este file .py faz o plot da elevação do terreno da Bacia Amazônica utilizando o 
# dado de tepodragia baixado do seguinte link: 
# https://topex.ucsd.edu/WWW_html/mar_topo.html
# https://topex.ucsd.edu/pub/global_topo_1min/
# Resolução espacial de aproximadamente: ~2 kilometer
# Resolução em Z: ~150 meters
#
'''

###########################################################################################

print("Run Code")
# Importando pacotes de python
print("1. Importando pacotes")
# Pacotes de processamento de dados
import xarray as xr
import numpy as np

# Importando pacotes de processamento de figuras
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.lines import Line2D as Line

# Pacotes para gerar a projeção dos mapas e formatar os eixos
import cartopy, cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
print("2. Pacotes lidos")

#############################################################################################

# Read dataset
print("3. Read dataset")
ds = xr.open_dataset('/home/ronaldrn/ronald/mestrado/topography/topo_23.1.nc')
# Fazendo um slice sobre a área da Bacia Amazônica
print("4. Fazendo um slice sobre a área da Bacia Amazônica")
ds_ba = ds.sel(lat=slice(-25, 10), lon=slice(-85, -45))

#############################################################################################

# Criando a figura para fazer o plot
print("4. Criando a figura para fazer o plot")
fig, ax = plt.subplots(figsize = (16,8), subplot_kw = {'projection': ccrs.PlateCarree()})

# Formatando os eixods do plot da Bacia Amazônica
print("5. Formatando os eixos do plot da Bacia Amazônica")
# Criando a linhas de grade para nosso plot
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
# Removendo os labels da grade do lado superior
gl.top_labels = False
# Removes os labels de grade do lado direito
gl.right_labels = False
# Estabelcendo o size dos labels no eixo X
gl.xlabel_style = {'size':14}
# Estabelecendo o size dos labels no eixo Y
gl.ylabel_style = {'size':14}
# Formatando os labels dos ticks como latitude e longitude (º)
gl.yformatter = LATITUDE_FORMATTER
gl.xformatter = LONGITUDE_FORMATTER

# Agregando os rios, estados, linhas de costa e linhas divisores dos paises
print("6. Agregando rios, estados, límites de paises e linhas de costa")
rivers_50m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m')
ax.add_feature(rivers_50m, facecolor = 'None', edgecolor = 'b', linewidth = 1)
# Agregando os límites entre paises
ax.add_feature(cfeature.BORDERS, edgecolor = '0.25')
# Agregando linhas de costa
ax.add_feature(cfeature.COASTLINE)
# Agregando os estado do Brasil
states_provinces = cfeature.NaturalEarthFeature(
    category = 'cultural',
    name = 'admin_1_states_provinces_lines',
    scale = '50m',
    facecolor = 'none'
)
ax.add_feature(states_provinces, edgecolor = 'gray')

# Agregando o shapefile da Bacia Amazônica
print("7. Agregando o shapefile da Bacia Amazônica")
fname = '/home/ronaldrn/ronald/mestrado/amazonas/Limite_Cuenca_Amazonas_geogpsperu_juansuyo.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())
ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='red', facecolor='none', alpha=1, linewidth=2)
# Agregando legenda
ax.set_title('Topography Configuration of Amazon Basin', y=1.04,size=22, fontweight='bold', fontfamily='sans')

#############################################################################################

# Criando a legenda
print("8. Criando legenda")
# Estabelecendo os cors das linhas na legenda
legend_artists = [Line([0], [0], color=color, linewidth=3) for color in ('black', 'gray', 'red', 'blue')]
# Estabelecendo os labels para cada cor na legenda
legend_texts = ['America do Sul', 'Estados do Brasil', 'Bacia da Amazônia', 'Rios']
# Agregando a legenda no plot
legend = ax.legend(legend_artists, legend_texts, fancybox=True, loc='lower left', framealpha=0.75, fontsize = 12)
# Estabelecendo cor de fondo da legenda
legend.legendPatch.set_facecolor('wheat')

#############################################################################################

# Insertando a seta do norte
print("9. Insertando seta em direção do Norte")
# Estabelecendo a posição e tamanho da seta
x, y, arrow_length = 0.95, 0.97, 0.08
# Configurando a seta com o label 'N', o color e forma
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=10, headwidth=25),
            ha='center', va='center', fontsize=25,
            xycoords=ax.transAxes)

#############################################################################################

# Agregando o plot da Elevação do terreno
print("10. Agregando o plot da topografia")
# Criando o plot no formato de contornos
altitude = ax.contourf(ds_ba.lon, ds_ba.lat, ds_ba.z, cmap="terrain", extend='min',\
    levels = np.arange(0, ds_ba.z.max(), 100), vmin=-2200)

# Adicionando a barra de cor
# Configurando a magnitude da barra de cores
cbar = plt.colorbar(altitude, ax=ax, ticks=np.arange(0, ds_ba.z.max(), 150), fraction = 0.035, pad=0.05)
# Configurando os labels da barra de cores e sua legenda
cbar.set_label('Elevation [m asl]', size = 16)
# Tamanho da legenda dos ticks ou valores
cbar.ax.tick_params(labelsize=12)

###############################################################################################

# Formatando o posicionamento do plot na figura
plt.subplots_adjust(hspace=1)
# Menos espaços em branco
fig.tight_layout()
# Fazendo uma pre-visualização
plt.show()
# Salvando a Figura
print("15. Salvando figuras dos parâmetros diurnos")
fig.savefig('/home/ronaldrn/ronald/mestrado/topography/topography_AmazonBasin.png', format='png', dpi = 100)
print("Figura Salvada")

print("Execução terminada do file topography_amazon_basin.py")
