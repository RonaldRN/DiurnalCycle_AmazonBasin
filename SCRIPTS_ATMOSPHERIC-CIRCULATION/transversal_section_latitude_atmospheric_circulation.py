"""
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# MSc. Student at Institute of Astronomy, Geophisycs and Atmospheric Sciences at University of São Paulo
# File: transversal_section_latitude_atmospheric_circulation.py 
#
# Descriptiopn:
# Esse script faz os gráficos dos cortes transversais para uma latitude constante da circulação atmosférica 
# utilizando as componentes zonal e meridional do vento (u,v), a velocidade vertical omega (w) e a umidade
# específica incluindo a topografia dos Andes. Os períodos eleitos são os meses de Janeiro, Abril, Julho e Outubro
# Nos horários de máximas taxas de precipitação.
# Os plots são baseados no arquivo de Ruiz-Hernándes et al. (2021)
#
"""
#
# -------------------------------------------------------------------------------------------------------------------
#
# Livrarias de leitura e processamento de dados
print("1. Ler os pacotes")
import xarray as xr
import numpy as np

# Importar pacotes de geração de figuras
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs # Pacote para mapas (sistema de referência cooordenado)
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
print("2. Terminou de ler os pacotes")

# --------------------------------------------------------------------------------------------------------
print("3. Ler os dados")
# Path dos dados
file_january = '/home/ronaldrn/ronald/mestrado/NETCDF_ATMOSPHERIC_CIRCULATION/local_circulation_january.nc'
file_april = '/home/ronaldrn/ronald/mestrado/NETCDF_ATMOSPHERIC_CIRCULATION/local_circulation_april.nc'
file_july = '/home/ronaldrn/ronald/mestrado/NETCDF_ATMOSPHERIC_CIRCULATION/local_circulation_july.nc'
file_october = '/home/ronaldrn/ronald/mestrado/NETCDF_ATMOSPHERIC_CIRCULATION/local_circulation_october.nc'

# Abrindo o arquivo NetCDF
print("--------------------------------------------------------------------")
print('                                                                    ')
print("DIGITAR O CÓDIGO DO PERÍODO DE INTERESSE:")
print('                                                                    ')
print("Janeiro: Janeiro")
print("Abril: Abril")
print("Julho: Julho")
print("Outubro: Outubro")
print('                                                                    ')
periodo = input("Digite o código do período em upper-case letters: ")

if periodo == "Janeiro":
    # Abrir o dado
    ds_january = xr.open_dataset(file_january)
    # Calcular a média
    ds_mean_january = ds_january.groupby('time.hour').mean(dim=['time'])
    # Fazer um corte sobre a região de interesse
    ds = ds_mean_january.sel(latitude = -13, longitude=slice(-80,-65))
    # Title
    title = ['Janeiro [2001-2020] ~ 3:30 HL', 'Janeiro [2001-2020] ~ 15:30 HL']
    # Hora UTC
    hour = [8, 20]

elif periodo == "Abril":
    # Abrir o dado
    ds_april = xr.open_dataset(file_april)
    # Calcular a média
    ds_mean_april = ds_april.groupby('time.hour').mean(dim=['time'])
    # Fazer um corte sobre a região de interesse
    ds = ds_mean_april.sel(latitude = -13, longitude=slice(-80,-65))
    # Title
    title = ['Abril [2001-2020] ~ 2:30 HL', 'Abril [2001-2020] ~ 15:30 HL']
    # Hora UTC
    hour = [7, 20]

elif periodo == "Julho":
    # Abrir o dado
    ds_july = xr.open_dataset(file_july)
    # Calcular a média
    ds_mean_july = ds_july.groupby('time.hour').mean(dim=['time'])
    # Fazer um corte sobre a região de interesse
    ds = ds_mean_july.sel(latitude = -13, longitude=slice(-80,-65))
    # Title
    title = ['Julho [2001-2020] ~ 2:30 HL', 'Julho [2001-2020] ~ 15:30 HL']
    # Hora UTC
    hour = [7, 20]

elif periodo == "Outubro":
    # Abrir o dado
    ds_october = xr.open_dataset(file_october)
    # Calcular a média
    ds_mean_october = ds_october.groupby('time.hour').mean(dim=['time'])
    # Fazer um corte sobre a região de interesse
    ds = ds_mean_october.sel(latitude = -13, longitude=slice(-80,-65))
    # Title
    title = ['Outubro [2001-2020] ~ 5:30 HL', 'Outubro [2001-2020] ~ 15:30 HL']
    # Hora UTC
    hour = [10, 20]

print("4. Abrir o dado de topografia")
# Ler o dado da topografia
ds_topo = xr.open_dataset('/home/ronaldrn/Downloads/topo_23.1.nc')
# Fazer um corte sobre a região de interesse
ds_ba = ds_topo.sel(lat=slice(-25, 10), lon=slice(-85, -45))

# ---------------------------------------------------------------------------------------------------
# CRIANDO A FIGURA E FORMATANDO O PLOT COM O PACOTE CARTOPY
print("5. Criando a figura")

print("6. Criando a figura e estabelecen 2 plots")
fig, ax = plt.subplots(1,2,figsize=(12,7), sharey = True)

# Criar a paleta de cores do plot
cmap = (mpl.colors.ListedColormap(['white','cyan','#7FFFD4','#BBF90F','#FFFF00','#FFA500','#F97306','#FF4500','#A52A2A']))
# Criar o rango de valores da paleta de cores
colorb = np.arange(0,18,2)

# CRIANDO O MAPA 1
print("7. Criando o mapa 1")
# Plot da umidade específica (shaded, g/Kg) 
q = ax[0].contourf(ds.longitude, ds.level, (ds['q']*1000).isel(hour=hour[0]), \
    levels= (colorb), vmax=18, extend='max', cmap=cmap)

# Plot do vento zonal (m/s) e vertical (cm/s) (vetores)
vetor = ax[0].quiver(ds.longitude, ds.level, ds['u'].isel(hour=hour[0]), \
    ds['w'].isel(hour=hour[0])*-10, color='black', width=0.0025, scale=150,\
    headlength=4, headwidth=3, minlength=0.05, minshaft=0.15)

# Invertemos o eixo do nível de pressão
plt.gca().invert_yaxis()
#Aplicando escala log
ax[0].set_yscale('log')
# Criando um array para formatar o límite do eixo X
xticks = np.arange(-80,-64,4)
# Criando um arrar para formatar o límite do eixo Y
yticks = np.arange(300,1100,100)
# FORMATANDO O PLOT COM AS FUNÇÕES DO CARTOPY
# Formatando os límites do eixo X <- Longitude
print("8. Formatação dos eixos")
ax[0].set_xticks(xticks) 
ax[0].set_xticklabels(xticks, fontsize = 14)
ax[0].xaxis.set_major_formatter(LongitudeFormatter())
# Formatando os límites do eixo Y <- Latitude
ax[0].set_yticks(yticks)
ax[0].set_yticklabels(yticks, fontsize=14)
ax[0].set_ylim([1000,300])
ax[0].set_ylabel('Nível de Pressão (hPa)', fontsize=14)
ax[0].set_title(title[0], y=1,size=16, fontweight='bold', fontfamily='sans')
# Criando o eixo Y (no lado direito) da altitude (metros)
print("9. Criando o eixo da topografia")
ax1 = ax[0].twinx()
# Plot da topografia
topo_line = ds_ba['z'].sel(lat=-13, method='nearest').plot(color='gray')
topografia = ds_ba['z'].sel(lat=-13, method='nearest')
plt.fill_between(ds_ba.lon, topografia, color='gray', alpha=0.8)
# Límites do eixo X da topografoa
ax1.set_xlim([-80,-65])
# Límites do eixo Y da altitude 
ax1.set_ylim([0,7000])
# Apagando o label do eixo Y do plot da esquerda
ax1.get_yaxis().set_visible(False)
# Título em branco do file da topografia
ax1.set_title('')

# ---------------------------------------------------------------------------------------------------
# CRIANDO O MAPA 2
print("10. Criando o mapa 2")
# Plot da umidade específica (shaded)
q = ax[1].contourf(ds.longitude, ds.level, (ds['q']*1000).isel(hour=hour[1]), \
    levels= (colorb), vmax=18, extend='max', cmap=cmap)

# Plot do vento zonal e vertical (vetores)
vetor = ax[1].quiver(ds.longitude, ds.level, (ds['u']).isel(hour=hour[1]), \
    ds['w'].isel(hour=hour[1])*-10, color='black', width=0.0025, scale=150,\
    headlength=4, headwidth=3, minlength=0.05, minshaft=0.15)

# Criando o rango de valores do eixo X
ax[1].set_xticks(xticks) 
# Labels do eixo X
ax[1].set_xticklabels(xticks, fontsize = 14)
# Formato de Longitudes do eixo X
ax[1].xaxis.set_major_formatter(LongitudeFormatter())
# Formatando os límites do eixo Y
ax[1].set_yticks(yticks)
# Labels do Eixo Y
ax[1].set_yticklabels(yticks, fontsize=14)
# Rango de valores do Eixo Y
ax[1].set_ylim([1000,300])
# Título do mapa 2
ax[1].set_title(title[1], y=1,size=16, fontweight='bold', fontfamily='sans')
# Criando o eixo Y (no lado direito) da altitude (metros)
print("11. Criando o exito da toipografia")
ax2 = ax[1].twinx()
# Plot da topografia
topo_line = ds_ba['z'].sel(lat=-13, method='nearest').plot(color='gray')
topografia = ds_ba['z'].sel(lat=-13, method='nearest')
plt.fill_between(ds_ba.lon, topografia, color='gray', alpha=0.8)
# Límites do eixo X da topografia
ax2.set_xlim([-80,-65])
# Límites do eixo Y da topografia
ax2.set_ylim([0,7000])
# Label do eixo Y da topografia
ax2.set_ylabel('Altitude (m)', fontsize=16)
# Título em branco
ax2.set_title('')
# Criando a paleta de cores dos plots
cbar = fig.colorbar(q, ax = ax[:], ticks = colorb, fraction=0.06, orientation='horizontal', pad=0.15, aspect=10)
# Label da paleta de cores da umidade específica
cbar.ax.tick_params(labelsize=14)
cbar.set_label('Specific humidity [g/kg]', size = 14, labelpad=-60)

# Criando a paleta de cores dos plots
#print("12. Criando a paleta de cores")
#if periodo == 'Outubro':
#    cbar = fig.colorbar(q, ax = ax[:], ticks = colorb, fraction=0.06, orientation='horizontal', pad=0.15, aspect=10)
    # Label da paleta de cores da umidade específica
#    cbar.set_label('Specific humidity [g/kg]', size = 14, labelpad=-60)

# Ajustar o plot
fig.tight_layout

plt.show()
print("13. Salvando a figura")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_CIRCULATION/CT_latitude_' + f'{periodo}.png', format='png', dpi = 300)
print("14. Terminou de rodar o código")