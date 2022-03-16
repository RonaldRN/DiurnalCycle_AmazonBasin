'''
#
# File: plot_composite_series_time.py
# Código em Python para fazer os plots das médias horárias (composites com dt = 30 min) 
# dos dados de precipitação. A análise será feita para o estudo do "Ciclo
# diurno da precipitação na Bacia Amazônica".
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mial: ronald.ramirez.nina@usp.br
# Estudante de Mestrado 
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Paulo
#
'''
print("RUN CODE")

# Import Packages 
print("1. Importando os pacotes")
# Importando pacotes de processamento de dados
import xarray as xr
import numpy as np
import pandas as pd

# Importando pacote de plot
import matplotlib.pyplot as plt

# Importando Funções Harmônica e LST
from harmonicFunction_TimeSeries import harmonico
from localsolartimeFunction import LST
print("2. Terminou de importar pacotes")
#
# ----------------------------------------------------------------------------------------------
# 
# Read Dataset
print("3. Read Dataset")
# Path of dataset
file_in = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_DJF.nc"
# Read dataset
ds = xr.open_dataset(file_in)
print("4. Terminou de ler o dataset")
#
# ----------------------------------------------------------------------------------------------
#
# Definindo as coordenadas geográficas Latitude e Longitude para a extração da série temporal
print("Extraindo a série temporal do arquivo NetCDF")
lat = -3.06
lon = -72.32
# Extraíndo série temporal do arquivo NetCDF
gridp = ds.sel(lat = lat, lon = lon, method = 'nearest').precipitationCal.values

# Aplicando a Função harmônica sobre o série temporal extraída
# Obtendo as Funções harmônicas 1º H e 2º H
print("5. Aplicando a Função harmônica para obtenção dos 1ºH e 2ºH")
YH1, YH2 = harmonico(gridp)

# Obtendo os parâmetros da Função harmônica para o 1º e 2º H
print("6. Aplicando a Função harmônica para obtenção dos parâmetros")
params = harmonico(gridp, onlycoef = True, harmonic = False)
#
# --------------------------------------------------------------------------------------------------
#
# Criando um DataFrame para armazenar os valores dos outputs da função harmônica
print("7. Criando um DataFrame")
df_YH = pd.DataFrame()
df_YH['utc'] = np.arange(0,24,0.5)
df_YH['pp'] = gridp
df_YH['YH1'] = YH1
df_YH['YH2'] = YH2
df_YH['lon'] = lon 
df_YH['LST'] = df_YH.apply(lambda x:LST(x['lon'], x['utc']), axis = 1)
df_YH.sort_values(['LST'], ascending=True, inplace=True)
df_YH = df_YH.round({'LST':2})
df_YH.set_index(['LST'], inplace=True)
print("8. Dataframe com o 1ºH e 2ºH finalizado")

# Criando DataFrame para armazenar os parâmetros harmônicos
print("9. Criando DataFrame")
df_params = pd.DataFrame()
df_params['index'] = np.arange(1,2,1)
df_params['lat'] = lat
df_params['lon'] = lon
df_params['C1_24h'] = params[0]
df_params['C2_24h'] = params[1]
df_params['F1_UTC'] = params[2]
df_params['F2_UTC'] = params[3]
df_params['F2_12UTC'] = params[4]
df_params['ppmean'] = params[5]
df_params['F1_LST'] = df_params.apply(lambda x:LST(x['lon'], x['F1_UTC']), axis = 1)
df_params['F2_LST'] = df_params.apply(lambda x:LST(x['lon'], x['F2_UTC']), axis = 1)
df_params['F2_12LST'] = df_params.apply(lambda x:LST(x['lon'], x['F2_12UTC']), axis = 1)
df_params = df_params.round({'C1_24h':2,'C2_24h':2,'F1_LST':2,'F2_LST':2,'F2_12LST':2})
print("10. DataFrame com os parâmetros finalizado")
#
# -----------------------------------------------------------------------------------------------
#
# Criando a figura para fazer o plot
fig, ax = plt.subplots(figsize = (8,5))
plt.plot(df_YH['pp'], 'k', label='pp')
plt.plot(df_YH['YH1'], 'r', ls='--', label='1ºH | AN:'+ f'{df_params["C1_24h"].values}' + ' |Fase:' + f'{df_params["F1_LST"].values}')
plt.plot(np.mean(df_YH['pp']) + df_YH['YH1'] + df_YH['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
plt.xlabel('Local Solar Time')
plt.ylabel('Precipitation (mm/hr)')
plt.title('Diurnal Cycle DJF - Lat:' + f'{abs(lat)}' + 'ºS Lon:' + f'{abs(lon)}' + 'ºW', size=16)
plt.grid(True)
plt.legend(fontsize = 10)

plt.show()

print("11. Salvando figura da sére temporal")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_TIME_SERIES_COMPOSITE/time_series_'+ f'{lat}' + f'{lon}'+'_DJF_BA.png', format='png', dpi = 100)

print("12. Finalizou de executar o código")