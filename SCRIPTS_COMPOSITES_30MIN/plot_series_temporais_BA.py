'''
#
# File: plot_series_temporais_BA.py
# Código em Python para fazer 17 plots (16 nas bordas e 1 no centro)  das médias horárias
# (composites com dt = 30 min), o plot do 1ºH + ppmean 
# e o plot do 1ºH + 2ºH + ppmean dos dados de precipitação. 
# A análise será feita para o estudo do "Ciclo diurno da precipitação na Bacia Amazônica".
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
file_DJF = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_DJF.nc"
file_MAM = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_MAM.nc"
file_JJA = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_JJA.nc"
file_SON = "/home/ronaldrn/ronald/mestrado/NETCDF_COMPOSITE_30MIN/composite_diurnal_30min_SON.nc"

# Abrindo o arquivo NetCDF
print("--------------------------------------------------------------------")
print('                                                                    ')
print("DIGITAR O CÓDIGO DO PERÍODO DE INTERESSE:")
print('                                                                    ')
print("DJF: Dezembro - Janeiro - Fevereiro (DJF)")
print("MAM: Março - Abril - Maio (MAM)")
print("JJA: Junho - Julho - Agosto (JJA)")
print("SON: Setembro - Outubro - Novembro (SON)")
print('                                                                    ')
periodo = input("Digite o código do período em upper-case letters: ")

print('                                                                    ')
print("--------------------------------------------------------------------")
print('                                                                    ')
print("Considerar os Andes: SIM")
print("Não considerar os Andes: NAO")
print('                                                                    ')
andes = input("Considera coordenadas da Cordilheira dos Andes (SIM ou NAO): ")
print('                                                                    ')

# Read dataset
if periodo == 'DJF':
    ds = xr.open_dataset(file_DJF)
    if andes == 'SIM':
        # Latitude e Longitude considerando os Andes
        lat = [-1.32,-3.3,1,-5,-5,-16.1,-17.45,-14,-15,-13,-5,-13.77,-13,-2,-9.5,-8.447258]
        lon = [-76.28,-72,-72,-70,-65,-66.73,-64,-64,-60,-57,-78,-73.81,-70.663321,-63,-66.739,-57]
        cluster = [2,1,4,1,3,6,6,2,4,3,6,5,1,4,2,2]
        setor = ['NW','NW','NW','C','C','SW','S','S','S','S','NW','SW','SW','C','C','C']

    else:
        # Latitude e Longitude sem considerar os Andes  
        lat = [3,4.279977,0,-1,-0.8597,-3.8,-4,-5.4,-5,-1,0.75,0.368947,-2.5,0.39788,-0.094217,-1.956206]
        lon = [-63,-60.571129,-57,-54,-50.4,-54.53,-53,-53,-51.38393,-55,-62,-67.853762,-55.54,-52.970968,-50.729194,-53.466879]
        cluster = [6,4,6,4,5,3,1,2,6,3,2,1,6,5,2,1]
        setor = ['N','N','NE','NE','NE','E','E','E','E','NE','N','N','E','NE','NE','NE']

elif periodo == 'MAM':
    ds = xr.open_dataset(file_MAM)
    if andes == 'SIM':
        # Latitudes e Longitudes considerando os Andes
        lat = [-1.23,-2,-3,-3,-13,-12,-14,-11.45,-16.83,-19,-4.52,-7,-13,-13,-10.5,-10.72]
        lon = [-78.56,-76.77,-75,-72,-52.16,-73,-74,-75,-65.28,-64,-78.17,-78.17,-70.663321,-54,-55.36,-58.26]
        cluster = [3,4,1,2,6,5,6,3,2,5,5,6,2,3,1,4]
        setor = ['NW','NW','NW','NW','S','SW','SW','SW','SW','S','NW','NW','SW','S','S','S']

    else:
        # Latitude e longitude sem considerar os Andes
        lat = [3,4.437964,0,0.9,0,-5,-3.41,-3.26,-2.40,-4,0.5,2.26,0.71,-0.55,-5,-5]
        lon = [-63,-60.539219,-55,-53.81,-51,-65,-69,-58.7,-62.67,-57.5,-63.9,-67.27,-68.39,-57.5,-53,-55]
        cluster = [5,3,1,3,4,1,2,4,3,4,4,2,1,2,2,1]
        setor = ['N','N','NE','NE','NE','C','C','C','C','E','N','N','N','NE','E','E']

elif periodo == 'JJA':
    ds = xr.open_dataset(file_JJA)
    if andes == 'SIM':
        # Latitudes e Longitudes considerando os Andes
        lat = [0,-3.5,-3,-2.5,-2.63,-15,-13.29,-18,-17,-13,0.37,-12.85,-13,-2.537,-2.83,-12]
        lon = [-77,-72,-69,-67,-62,-66,-64.51,-63,-61,-60,-77.54,-74.34,-70.663321,-59.52,-58.17,-56]
        cluster = [2,5,5,2,3,4,3,6,4,1,6,1,6,1,4,'X']
        setor = ['NW','NW','C','C','C','SW','S','S','S','S','NW','SW','SW','C','C','S']
    
    else:
        # Latitude e longitude sem considerar os Andes
        lat = [3.18,4.49,0.8,2,0.22,2.887,-5,-5.45,-5,-5,0.71,1.34,2.4,-1.67,-1.28,-3]
        lon = [-61.07,-59.81,-57.5,-55,-50.85,-63.45,-59,-53.81,-51,-53,-65,-65.58,-67.61,-57.34,-55.45,-52]
        cluster = [2,6,6,3,5,4,3,4,1,3,5,3,2,4,1,6]
        setor = ['N','N','NE','NE','NE','N','E','E','E','E','N','N','N','NE','NE','E']
        
elif periodo == 'SON':
    ds = xr.open_dataset(file_SON)
    if andes == 'SIM':
        # Latitudes e longitudes considerando os Andes
        lat = [1,-3,-3.36,-2.5,-2.73,-15,-18.2,-17,-13,-13,-3.55,-13.87,-18.5,-5,-2.34,-2.73]
        lon = [-73,-73.3,-72,-69,-67.32,-68.68,-63,-62,-60,-56,-77.25,-68.63,-66,-65,-61.85,-57.78]
        cluster = [4,3,6,3,6,1,2,7,1,4,7,2,5,4,1,7]
        setor = ['NW','NW','NW','C','C','SW','S','S','S','S','NW','SW','SW','C','C','C']
    
    else:
        # Latitudes e longitudes sem considerar os Andes
        lat = [3.52,3.23,5,1,0,0.27,1.53,-13,-4,-5.83,2,2.31,1,-1.37,-5,-5]
        lon = [-62.38,-61.07,-60,-55,-51,-66.55,-60,-52.74,-52,-53,-63,-67.61,-69.36,-53,-55,-51]
        cluster = [2,4,1,2,5,4,1,4,2,1,7,6,3,1,4,7]
        setor = ['N','N','N','NE','NE','N','N','SE','E','E','N','N','N','NE','E','E']

print("4. Terminou de ler o dataset")
#
# ----------------------------------------------------------------------------------------------
#
# Criando uma lista de DataFrames onde armazenar os dados da ppmean, 1ºH e 2ºH para os 16 pontos selecioandos
df_YH = ['df1_YH','df2_YH','df3_YH','df4_YH','df5_YH','df6_YH','df7_YH','df8_YH',\
    'df9_YH','df10_YH','df11_YH','df12_YH','df13_YH','df14_YH','df15_YH','df16_YH']

# Criando uma lista de DataFrames para armazenar os parâmetros harmônicos dos 16 pontos selecionados
df_params = ['df1_params','df2_params','df3_params','df4_params','df5_params','df6_params','df7_params','df8_params',\
    'df9_params','df10_params','df11_params','df12_params','df13_params','df14_params','df15_params','df16_params']

# Extraíndo a série temporal do arquivo NetCDF
print("5. Extraindo a série temporal do arquivo NetCDF")
# Criando uma lista vazia para armazenar os gridpoints
gridpoints = []
for i in np.arange(1,17):
    gridp = ds.sel(lat = lat[i-1], lon = lon[i-1], method = 'nearest').precipitationCal.values
    gridpoints.append(gridp)

# Aplicando a Função Harmônica para cada gridpoint
print("6. Aplicando a Função harmônica para cada gridpoint")
for i in np.arange(1,17):
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
fig = plt.figure(figsize = (15,15))
grid = plt.GridSpec(5,5, wspace = 0.25, hspace = 0.95)

# Plot da imagem do centro 
plt.subplot(grid[1:4,1:4])
plt.plot(df_YH[0]['pp'], 'k', label = 'pp')
plt.plot(np.mean(df_YH[0]['pp']) + df_YH[0]['YH1'], 'r', ls='--',\
    label='1ºH | AN:'+ f'{df_params[0]["C1_24h"].values}' + ' |Fase:' + f'{df_params[0]["F1_LST"].values}')
plt.plot(np.mean(df_YH[0]['pp']) + df_YH[0]['YH1'] + df_YH[0]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
plt.xticks(range(0,25,3))
plt.grid(True)
plt.legend(fontsize = 14)


# Fazendo uma aproximação a duas decimais das latitudes e longitudes
print("8. Fazendo uma aproximação a duas decimais das lats e lons")
lat_2d = [round(item,2) for item in lat]
lon_2d = [round(iten,2) for iten in lon]

# Plots da primeria fila dos plots Fila: 0 | Coluna:0-5
print("9. Plots - Fila: 0 | Coluna: 0-4")
for i in np.arange(1,6):

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
        plt.title('Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title('Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da última fila dos plots Fila: 4 | Coluna: 0-5
print("10. Plots - Fila: 4 | Coluna: 0-4")
for i in np.arange(6,11):

    plt.subplot(grid[4,i-6])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title('Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title('Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da primeira coluna Fila: 1-3 | Coluna: 0
print("11. Plots - Fila: 1-3 | Coluna: 0")
for i in np.arange(11,14):

    plt.subplot(grid[i-10,0])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title('Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title('Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Plots da última coula Fila: 1-3 | Coluna: 4
print("12. Plots - Fila: 1-3 | Coluna: 4")
for i in np.arange(14,17):

    plt.subplot(grid[i-13,4])
    plt.plot(df_YH[i-1]['pp'], 'k', label = 'pp')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'], 'r', ls='--', label='1ºH + ppmean')
    plt.plot(np.mean(df_YH[i-1]['pp']) + df_YH[i-1]['YH1'] + df_YH[i-1]['YH2'], 'b', ls='--', label='ppmean + 1ºH + 2ºH')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.2))
    plt.xticks(range(0,25,3))
    plt.xlabel('Local Solar Time')
    plt.ylabel('(mm/hr)')
    if lat_2d[i-1] >= 0:
        plt.title('Lat:' + f'{lat_2d[i-1]}' + 'ºN Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    else:
        plt.title('Lat:' + f'{abs(lat_2d[i-1])}' + 'ºS Lon:' + f'{abs(lon_2d[i-1])}' + 'ºW | ' + f'C:{cluster[i-1]} | ' + f'R:{setor[i-1]}\n' + \
            'AN:'+ f'{df_params[i-1]["C1_24h"].values}' + ' | Fase:' + f'{df_params[i-1]["F1_LST"].values}' + \
                ' | pp:' + f'{df_params[i-1]["ppmean"].values}', size=10)
    #plt.grid(True)
    #plt.legend(fontsize = 6)

# Fazendo a legenda das curvas na parte inferior central da Figura
print("13. Legenda das curvas dos plots")
plt.legend(bbox_to_anchor = (0.5,0.025),loc = 'lower center', ncol = 3, bbox_transform = fig.transFigure, frameon = False)

plt.show()

print("14. Salvando figura da sére temporal")
fig.savefig('/home/ronaldrn/ronald/mestrado/PLOTS_TIME_SERIES_COMPOSITE/SeriesTemporais_' + f'Andes{andes}_' + f'{periodo}_BA.png',\
     format='png', dpi = 300)

print("15. Finalizou de executar o código")