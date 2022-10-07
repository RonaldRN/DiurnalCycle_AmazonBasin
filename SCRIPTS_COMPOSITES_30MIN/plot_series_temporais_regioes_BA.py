'''
#
# File: plot_series_temporais_regioes_BA.py
# Código em Python para fazer 24 plots das médias horárias
# (composites com dt = 30 min), o plot do 1ºH + ppmean 
# e o plot do 1ºH + 2ºH + ppmean dos dados de precipitação dos dados de precipitação. 
# A análise será feita para o estudo do "Ciclo diurno da precipitação nas sub-regiões da
# Bacia Amazônica".
#
# Autor: Ronald Guiuseppi Ramírez Nina
# e-mial: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
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
file_DJF = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_DJF.nc"
file_MAM = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_MAM.nc"
file_JJA = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_JJA.nc"
file_SON = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_SON.nc"

ds_DJF = xr.open_dataset(file_DJF)
ds_MAM = xr.open_dataset(file_MAM)
ds_JJA = xr.open_dataset(file_JJA)
ds_SON = xr.open_dataset(file_SON)

# Abrindo o arquivo NetCDF
print("--------------------------------------------------------------------")
print('                                                                    ')
print("DIGITAR O CÓDIGO DO SETOR DE INTERESSE:")
print('                                                                    ')
print("NE: Nordeste da BA")
print("E: Leste da BA")
print("N: Norte da BA")
print("C: Centro da BA")
print("S: Sul da BA")
print("NW: Noroeste da BA")
print("SW: Sudoeste da BA")
print('                                                                    ')
setor = input("Digite o código do setor da BA em upper-case letters: ")

print('                                                                    ')
print("--------------------------------------------------------------------")
print('                                                                    ')

# Read dataset
if setor == 'NE':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-1.956206,-0.094217,-1,-1,-0.8597,0,0,-0.55,0.9,0,-1,-1.18,-1.28,2,-1.67,0.22,0.8,-1.25,-1.37,1,0,-0.5,0.5,0.93]
    lon = [-53.466879,-50.729194,-55,-54,-50.40,-57,-55,-57.5,-53.81,-51,-54,-56.81,-55.45,-55,-57.34,-50.85,-57.5,-55.40,-53,-55,-51,-56.4,-57.7,-58.21]
    cluster = [1,2,3,4,5,6,1,2,3,4,1,2,1,3,4,5,6,1,1,2,5,1,2,4]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'E':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-4,-5.40,-3.80,-2.5,-5,-5,-5,-5,-4,-5.44,-2.1,-3,-5,-2.12,-5,-5.54,-3.38,-3,-5.83,-4,-5.85,-5,-13,-5]
    lon = [-53,-53,-54.53,-55.54,-51.38393,-58,-55,-53,-57.5,-50.99,-52.16,-58.65,-51,-55.598,-59,-53.81,-58.75,-52,-53,-52,-56.91,-55,-52.74,-51]
    cluster = [1,2,3,6,6,2,1,2,4,5,1,4,1,2,3,4,5,6,1,2,3,4,4,7]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'N':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [0.368947,0.75,0.25,4.279977,1.22,3,0.71,2.26,4.437964,0.5,3,1.25,2.4,3.18,1.34,2.887,0.71,4.49,5,3.52,1,0.27,2.31,2]
    lon = [-67.853762,-62,-67.13,-60.571129,-65.58,-63,-68.39,-67.27,-60.539219,-63.9,-63,-65.82,-67.61,-61.07,-65.58,-63.45,\
        -65,-59.81,-60,-62.38,-69.36,-66.55,-67.61,-63]
    cluster = [1,2,3,4,5,6,1,2,3,4,5,3,2,2,3,4,5,6,1,2,3,4,6,7]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'C':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-5,-8.447258,-9.5,-5,-2,-3.20,-5,-3.41,-2.4,-3.26,-2.41,-3,-2.537,-2.5,-2.63,-2.83,-3,-4,-2.34,-2.5,-5,-2.73,-2.73,-4]
    lon = [-70,-57,-66.739,-65,-63,-60,-65,-69,-62.67,-58.7,-67.85,-60,-59.52,-67,-62,-58.17,-69,-64.32,-61.85,-69,-65,-67.32,-57.78,-66]
    cluster = [1,2,2,3,4,2,1,2,3,4,4,4,1,2,3,4,5,4,1,3,4,6,7,4]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'S':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-19.08,-14,-13,-20,-15,-17.45,-10.5,-10,-13,-10.72,-19,-13,-13,-13.29,-17,-18,-12,-20,-13,-18.2,-13,-20,-16.75,-17]
    lon = [-63.69,-64,-57,-64,-60,-64,-55.36,-57.2,-54,-58.26,-64,-52.16,-60,-64.51,-61,-63,-56,-64,-60,-63,-56,-64.17,-64.66,-62]
    cluster = [1,2,3,3,4,6,1,2,3,4,5,6,1,3,4,6,'X','X',1,2,4,5,6,7]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'NW':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-3.3,-1.32,-3,1,-6.48,-5,-3,-3,-1.23,-2,-4.52,-7,-6.3,0,-6,-7,-3.5,0.37,-6.43,-5.27,-3,1,-3.36,-3.55]
    lon = [-72,-76.28,-74.15,-72,-77.78,-78,-75,-72,-78.56,-76.77,-78.17,-78.17,-78.07,-77,-73.5,-76,-72,-77.54,-77.93,-78.61,-73.3,-73,-72,-77.25]
    cluster = [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,6,7]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

elif setor == 'SW':

    # Período DJF: Posições     00 - 05
    # Período MAM: Posições     06 - 11
    # Período JJA: Posições     12 - 17
    # Período SON: Posições     18 - 23
    lat = [-13,-16.5,-12,-18.4,-13.77,-16.1,-13,-16.8,-11.45,-12,-12,-14,-13,-16.8,-12.85,-11.4,-15,-14,-13,-16.8,-15,-13.87,-10.55,-18.5]
    lon = [-70.663321,-65.77,-67,-65.77,-73.81,-66.73,-70.663321,-65.33,-75,-67,-73,-74,-70.663321,-65.63,-74.34,-75,-66,-73.67,-70,-65.2,\
        -68.68,-68.63,-66.3,-66]
    cluster = [1,1,2,4,5,6,2,2,3,3,5,6,6,6,1,3,4,'X',6,6,1,2,4,5]
    periodo = ['DJF','DJF','DJF','DJF','DJF','DJF','MAM','MAM','MAM','MAM','MAM','MAM',\
        'JJA','JJA','JJA','JJA','JJA','JJA','SON','SON','SON','SON','SON','SON']
    letter = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)']

print("4. Terminou de ler o dataset")
#
# ----------------------------------------------------------------------------------------------
#
# Criando uma lista de DataFrames onde armazenar os dados da ppmean, 1ºH e 2ºH para os 24 pontos selecioandos
df_YH = ['df1_YH','df2_YH','df3_YH','df4_YH','df5_YH','df6_YH','df7_YH','df8_YH','df9_YH','df10_YH','df11_YH','df12_YH',\
    'df13_YH','df14_YH','df15_YH','df16_YH','df17_YH','df18_YH','df19_YH','df20_YH','df21_YH','df22_YH','df23_YH','df24_YH']

# Criando uma lista de DataFrames para armazenar os parâmetros harmônicos dos 24 pontos selecionados
df_params = ['df1_params','df2_params','df3_params','df4_params','df5_params','df6_params','df7_params','df8_params',\
    'df9_params','df10_params','df11_params','df12_params','df13_params','df14_params','df15_params','df16_params',\
        'df17_params','df18_params','df19_params','df20_params','df21_params','df22_params','df23_params','df24_params']

# Extraíndo a série temporal do arquivo NetCDF
print("5. Extraindo a série temporal do arquivo NetCDF")
# Criando uma lista vazia para armazenar os gridpoints
gridpoints = []
for i in np.arange(1,7):
    gridp = ds_DJF.sel(lat = lat[i-1], lon = lon[i-1], method = 'nearest').precipitationCal.values
    gridpoints.append(gridp)

for i in np.arange(7,13):
    gridp = ds_MAM.sel(lat = lat[i-1], lon = lon[i-1], method = 'nearest').precipitationCal.values
    gridpoints.append(gridp)

for i in np.arange(13,19):
    gridp = ds_JJA.sel(lat = lat[i-1], lon = lon[i-1], method = 'nearest').precipitationCal.values
    gridpoints.append(gridp)

for i in np.arange(19,25):
    gridp = ds_SON.sel(lat = lat[i-1], lon = lon[i-1], method = 'nearest').precipitationCal.values
    gridpoints.append(gridp)

# Aplicando a Função Harmônica para cada gridpoint
print("6. Aplicando a Função harmônica para cada gridpoint")
for i in np.arange(1,25):
    YH1, YH2 = harmonico(gridpoints[i-1])
    params = harmonico(gridpoints[i-1], onlycoef = True, harmonic = False)

    df_YH[i-1] = pd.DataFrame()
    df_YH[i-1]['utc'] = np.arange(0,24,0.5)
    df_YH[i-1]['pp'] = gridpoints[i-1]
    df_YH[i-1]['YH1'] = YH1
    df_YH[i-1]['YH2'] = YH2
    df_YH[i-1]['lon'] = lon[i-1] 
    df_YH[i-1]['LST'] = df_YH[i-1].apply(lambda x:LST(x['lon'], x['utc']), axis = 1)
    df_YH[i-1].sort_values(['LST'], ascending=True, inplace=True)
    df_YH[i-1] = df_YH[i-1].round({'LST':2})
    df_YH[i-1].set_index(['LST'], inplace=True)

    df_params[i-1] = pd.DataFrame()
    df_params[i-1]['index'] = np.arange(1,2,1)
    df_params[i-1]['lat'] = lat[i-1]
    df_params[i-1]['lon'] = lon[i-1]
    df_params[i-1]['C1_24h'] = params[0]
    df_params[i-1]['C2_24h'] = params[1]
    df_params[i-1]['F1_UTC'] = params[2]
    df_params[i-1]['F2_UTC'] = params[3]
    df_params[i-1]['F2_12UTC'] = params[4]
    df_params[i-1]['ppmean'] = params[5]
    df_params[i-1]['F1_LST'] = df_params[i-1].apply(lambda x:LST(x['lon'], x['F1_UTC']), axis = 1)
    df_params[i-1]['F2_LST'] = df_params[i-1].apply(lambda x:LST(x['lon'], x['F2_UTC']), axis = 1)
    df_params[i-1]['F2_12LST'] = df_params[i-1].apply(lambda x:LST(x['lon'], x['F2_12UTC']), axis = 1)
    df_params[i-1] = df_params[i-1].round({'lat':2,'lon':2,'C1_24h':2,'C2_24h':2,'F1_LST':2,'F2_LST':2,'F2_12LST':2,'ppmean':2})

# ------------------------------------------------------------------------------------------------------------------
# Criando a figura
print("7. Criando a figura")
fig = plt.figure(figsize = (20,15))
grid = plt.GridSpec(4,6, wspace = 0.25, hspace = 0.95)

# Fazendo uma aproximação a duas decimais das latitudes e longitudes
print("8. Fazendo uma aproximação a duas decimais das lats e lons")
lat_2d = [round(item,2) for item in lat]
lon_2d = [round(iten,2) for iten in lon]

# Plots da primeria fila dos plots Fila: 0 | Coluna:0-5
print("9. Plots - Fila: 0 | Coluna: 0-5")
for i in np.arange(1,7):

    plt.subplot(grid[0,i-1])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da última fila dos plots Fila: 1 | Coluna: 0-5
print("10. Plots - Fila: 1 | Coluna: 0-5")
for i in np.arange(7,13):

    plt.subplot(grid[1,i-7])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da primeira coluna Fila: 2 | Coluna: 0-5
print("11. Plots - Fila: 2 | Coluna: 0-5")
for i in np.arange(13,19):

    plt.subplot(grid[2,i-13])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da última coula Fila: 3 | Coluna: 0-5
print("12. Plots - Fila: 3 | Coluna: 0-5")
for i in np.arange(19,25):

    plt.subplot(grid[3,i-19])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title(f'{letter[i-1]}' + 'Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW|' + f'C:{cluster[i-1]}|' + f'P:{periodo[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Fazendo a legenda das curvas na parte inferior central da Figura
print("13. Legenda das curvas dos plots")
plt.legend(bbox_to_anchor = (0.5,0.025),loc = 'lower center', ncol = 3, bbox_transform = fig.transFigure, frameon = False)

plt.show()

print("14. Salvando figura da sére temporal")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_TIME_SERIES_COMPOSITE/SeriesTemporais_' + f'Setor_{setor}_BA.png', format='png', dpi = 300)

print("15. Finalizou de executar o código")