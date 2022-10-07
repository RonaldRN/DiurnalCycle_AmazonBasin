'''
#
# File: plot_criterio_easterling_robinson1985.py
# Código em Python para fazer os plots das médias horárias (composites com dt = 30 min) 
# dos dados de precipitação. O objetivo deste código é fazer um plot representando o 
# critério de Easterling e Robinson (1985) da amplitude normalizada (1ºH) sobre o
#  "Ciclo diurno da precipitação na Bacia Amazônica".
# 
# AN < 0,5 : A distribuição diurna da precipitação é bimodal (dois picos) ou uniforme (sem nenhum pico) no dia.
# AN > 0,5 : A distribuição diurna da precipitação é unimodal com um pico claro no dia. 
# AN > 1.0 : A distribuição diurna da precipitação é unimodal com um pico sobresaliente no dia.
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
lat = [-5, 0, -14.5]    # Ampl. Norm < 0.5 | [0.5 - 1] | > 1.0
lon = [-70, -65, -74]   # Ampl. Norm < 0.5 | [0.5 - 1] | > 1.0
# Extraíndo série temporal do arquivo NetCDF
# Amplitude Normalizada: < 0.5
gridp1 = ds.sel(lat = lat[0], lon = lon[0], method = 'nearest').precipitationCal.values
# Amplitude Normalizada: [0.5 - 1]
gridp2 = ds.sel(lat = lat[1], lon = lon[1], method = 'nearest').precipitationCal.values
# Amplitude Normnalizada: > 1.0
gridp3 = ds.sel(lat = lat[2], lon = lon[2], method = 'nearest').precipitationCal.values

# -----------------------------------------------------------------------------------------------
# SÉRIE TEMPORAL 1: # Amplitude Normalizada: < 0.5

# Aplicando a Função harmônica sobre o série temporal extraída
# Obtendo as Funções harmônicas 1º H e 2º H
print("*. SÉRIE TEMPORAL 1: # Amplitude Normalizada: < 0.5")
print("5. Aplicando a Função harmônica para obtenção dos 1ºH e 2ºH")
YH1, YH2 = harmonico(gridp1)

# Obtendo os parâmetros da Função harmônica para o 1º e 2º H
print("6. Aplicando a Função harmônica para obtenção dos parâmetros")
params = harmonico(gridp1, onlycoef = True, harmonic = False)
#
# Criando um DataFrame para armazenar os valores dos outputs da função harmônica
print("7. Criando um DataFrame")
df1_YH = pd.DataFrame()
df1_YH['utc'] = np.arange(0,24,0.5)
df1_YH['pp'] = gridp1
df1_YH['YH1'] = YH1
df1_YH['YH2'] = YH2
df1_YH['lon'] = lon[0] 
df1_YH['LST'] = df1_YH.apply(lambda x:LST(x['lon'], x['utc']), axis = 1)
df1_YH.sort_values(['LST'], ascending=True, inplace=True)
df1_YH = df1_YH.round({'LST':2})
df1_YH.set_index(['LST'], inplace=True)
print("8. Dataframe com o 1ºH e 2ºH finalizado")

# Criando DataFrame para armazenar os parâmetros harmônicos
print("9. Criando DataFrame")
df1_params = pd.DataFrame()
df1_params['index'] = np.arange(1,2,1)
df1_params['lat'] = lat[0]
df1_params['lon'] = lon[0]
df1_params['C1_24h'] = params[0]
df1_params['C2_24h'] = params[1]
df1_params['F1_UTC'] = params[2]
df1_params['F2_UTC'] = params[3]
df1_params['F2_12UTC'] = params[4]
df1_params['ppmean'] = params[5]
df1_params['F1_LST'] = df1_params.apply(lambda x:LST(x['lon'], x['F1_UTC']), axis = 1)
df1_params['F2_LST'] = df1_params.apply(lambda x:LST(x['lon'], x['F2_UTC']), axis = 1)
df1_params['F2_12LST'] = df1_params.apply(lambda x:LST(x['lon'], x['F2_12UTC']), axis = 1)
df1_params = df1_params.round({'C1_24h':2,'C2_24h':2,'F1_LST':2,'F2_LST':2,'F2_12LST':2})
print("10. DataFrame com os parâmetros finalizado")

# -----------------------------------------------------------------------------------------------
# SÉRIE TEMPORAL 2: # Amplitude Normalizada: [0.5 - 1]

# Aplicando a Função harmônica sobre o série temporal extraída
# Obtendo as Funções harmônicas 1º H e 2º H
print("*. SÉRIE TEMPORAL 2: # Amplitude Normalizada: [0.5 - 1]")
print("11. Aplicando a Função harmônica para obtenção dos 1ºH e 2ºH")
YH1, YH2 = harmonico(gridp2)

# Obtendo os parâmetros da Função harmônica para o 1º e 2º H
print("12. Aplicando a Função harmônica para obtenção dos parâmetros")
params = harmonico(gridp2, onlycoef = True, harmonic = False)
#
# Criando um DataFrame para armazenar os valores dos outputs da função harmônica
print("13. Criando um DataFrame")
df2_YH = pd.DataFrame()
df2_YH['utc'] = np.arange(0,24,0.5)
df2_YH['pp'] = gridp2
df2_YH['YH1'] = YH1
df2_YH['YH2'] = YH2
df2_YH['lon'] = lon[1] 
df2_YH['LST'] = df2_YH.apply(lambda x:LST(x['lon'], x['utc']), axis = 1)
df2_YH.sort_values(['LST'], ascending=True, inplace=True)
df2_YH = df2_YH.round({'LST':2})
df2_YH.set_index(['LST'], inplace=True)
print("13. Dataframe com o 1ºH e 2ºH finalizado")

# Criando DataFrame para armazenar os parâmetros harmônicos
print("14. Criando DataFrame")
df2_params = pd.DataFrame()
df2_params['index'] = np.arange(1,2,1)
df2_params['lat'] = lat[1]
df2_params['lon'] = lon[1]
df2_params['C1_24h'] = params[0]
df2_params['C2_24h'] = params[1]
df2_params['F1_UTC'] = params[2]
df2_params['F2_UTC'] = params[3]
df2_params['F2_12UTC'] = params[4]
df2_params['ppmean'] = params[5]
df2_params['F1_LST'] = df2_params.apply(lambda x:LST(x['lon'], x['F1_UTC']), axis = 1)
df2_params['F2_LST'] = df2_params.apply(lambda x:LST(x['lon'], x['F2_UTC']), axis = 1)
df2_params['F2_12LST'] = df2_params.apply(lambda x:LST(x['lon'], x['F2_12UTC']), axis = 1)
df2_params = df2_params.round({'C1_24h':2,'C2_24h':2,'F1_LST':2,'F2_LST':2,'F2_12LST':2})
print("15. DataFrame com os parâmetros finalizado")

# -----------------------------------------------------------------------------------------------
# SÉRIE TEMPORAL 3: # Amplitude Normalizada: > 1.0

# Aplicando a Função harmônica sobre o série temporal extraída
# Obtendo as Funções harmônicas 1º H e 2º H
print("*. SÉRIE TEMPORAL 3: # Amplitude Normalizada: > 1.0")
print("16. Aplicando a Função harmônica para obtenção dos 1ºH e 2ºH")
YH1, YH2 = harmonico(gridp3)

# Obtendo os parâmetros da Função harmônica para o 1º e 2º H
print("17. Aplicando a Função harmônica para obtenção dos parâmetros")
params = harmonico(gridp3, onlycoef = True, harmonic = False)
#
# Criando um DataFrame para armazenar os valores dos outputs da função harmônica
print("18. Criando um DataFrame")
df3_YH = pd.DataFrame()
df3_YH['utc'] = np.arange(0,24,0.5)
df3_YH['pp'] = gridp3
df3_YH['YH1'] = YH1
df3_YH['YH2'] = YH2
df3_YH['lon'] = lon[2] 
df3_YH['LST'] = df3_YH.apply(lambda x:LST(x['lon'], x['utc']), axis = 1)
df3_YH.sort_values(['LST'], ascending=True, inplace=True)
df3_YH = df3_YH.round({'LST':2})
df3_YH.set_index(['LST'], inplace=True)
print("19. Dataframe com o 1ºH e 2ºH finalizado")

# Criando DataFrame para armazenar os parâmetros harmônicos
print("20. Criando DataFrame")
df3_params = pd.DataFrame()
df3_params['index'] = np.arange(1,2,1)
df3_params['lat'] = lat[2]
df3_params['lon'] = lon[2]
df3_params['C1_24h'] = params[0]
df3_params['C2_24h'] = params[1]
df3_params['F1_UTC'] = params[2]
df3_params['F2_UTC'] = params[3]
df3_params['F2_12UTC'] = params[4]
df3_params['ppmean'] = params[5]
df3_params['F1_LST'] = df3_params.apply(lambda x:LST(x['lon'], x['F1_UTC']), axis = 1)
df3_params['F2_LST'] = df3_params.apply(lambda x:LST(x['lon'], x['F2_UTC']), axis = 1)
df3_params['F2_12LST'] = df3_params.apply(lambda x:LST(x['lon'], x['F2_12UTC']), axis = 1)
df3_params = df3_params.round({'C1_24h':2,'C2_24h':2,'F1_LST':2,'F2_LST':2,'F2_12LST':2})
print("21. DataFrame com os parâmetros finalizado")

#
# -----------------------------------------------------------------------------------------------
#
# Criando a figura para fazer o plot
print("22. Criando a figura")
fig, ax = plt.subplots(3,1,figsize = (8,12), sharex = True)

# Primeiro plot da Série Temporal 1
print("23. SÉRIE TEMPORAL 1: # Amplitude Normalizada: < 0.5")
ax[0].plot(df1_YH['pp'], 'k', label='pp')
ax[0].plot(df1_YH['YH1'], 'r', ls='--', label='1ºH | AN:'+ f'{df1_params["C1_24h"].values}' + ' |Fase:' + f'{df1_params["F1_LST"].values}')
ax[0].plot(np.mean(df1_YH['pp']) + df1_YH['YH1'] + df1_YH['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
#ax[0].set_xlabel('Local Solar Time')
ax[0].set_ylabel('Precipitation (mm/hr)')
ax[0].set_title('a) Diurnal Cycle DJF - Lat:' + f'{abs(lat[0])}' + 'ºS Lon:' + f'{abs(lon[0])}' + 'ºW', size=16)
ax[0].grid(True)
ax[0].legend(fontsize = 10)

print("24. SÉRIE TEMPORAL 2: # Amplitude Normalizada: [0.5 - 1]")
ax[1].plot(df2_YH['pp'], 'k', label='pp')
ax[1].plot(df2_YH['YH1'], 'r', ls='--', label='1ºH | AN:'+ f'{df2_params["C1_24h"].values}' + ' |Fase:' + f'{df2_params["F1_LST"].values}')
ax[1].plot(np.mean(df2_YH['pp']) + df2_YH['YH1'] + df2_YH['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
#ax[1].set_xlabel('Local Solar Time')
ax[1].set_ylabel('Precipitation (mm/hr)')
ax[1].set_title('b) Diurnal Cycle DJF - Lat:' + f'{abs(lat[1])}' + 'ºS Lon:' + f'{abs(lon[1])}' + 'ºW', size=16)
ax[1].grid(True)
ax[1].legend(fontsize = 10)

print("25. SÉRIE TEMPORAL 3: # Amplitude Normalizada: > 1.0")
ax[2].plot(df3_YH['pp'], 'k', label='pp')
ax[2].plot(df3_YH['YH1'], 'r', ls='--', label='1ºH | AN:'+ f'{df3_params["C1_24h"].values}' + ' |Fase:' + f'{df3_params["F1_LST"].values}')
ax[2].plot(np.mean(df3_YH['pp']) + df3_YH['YH1'] + df3_YH['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
ax[2].set_xlabel('Local Solar Time', size = 14)
ax[2].set_ylabel('Precipitation (mm/hr)')
ax[2].set_title('c) Diurnal Cycle DJF - Lat:' + f'{abs(lat[2])}' + 'ºS Lon:' + f'{abs(lon[2])}' + 'ºW', size=16)
ax[2].grid(True)
ax[2].legend(fontsize = 10)

fig.tight_layout()
plt.show()

print("26. Salvando figura da sére temporal")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_TIME_SERIES_COMPOSITE/criterio_easterling_robinson1985_DJF_BA.png', format='png', dpi = 100)

print("27. Finalizou de executar o código")