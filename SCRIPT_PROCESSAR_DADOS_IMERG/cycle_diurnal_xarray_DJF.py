'''
Versão 1

Código em Python para calcular as Amplitudes e Fases dos
Harmônicos 1º e 2º, mediante a metodologia estabelecida de
Wilks (2011). A análise será feita para o estudo do "Ciclo
diurno da precipitação na Bacia Amazônica" para o período de DJF.

Autor: Ronald Guiuseppi Ramírez Nina
Estudante de Mestrado 
Departamento de Ciências Atmosféricas IAG - USP
Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Paulo

'''

# Importando livrarias
print('Rodando código para o período de DJF')

print('1. Read packages')
import h5netcdf
from numpy.lib.function_base import _parse_gufunc_signature # Para ler o netcdf

# Livrarias de processamento
import xarray as xr # Pangeo (read rasterio)
from scipy.signal import *
import math
import pandas as pd
import numpy as np
import rioxarray # Para o Sist. Referência de coordenadas en xr

# Importando a Função harmônica e LST
from harmonicFunction import harmonico
from localsolartimeFunction import LST

# Plots
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import collections
import matplotlib.patches as mpatches
import calendar

print('2. End to read packages')
# -------------------------------------------------------------------------------------------------

# Abrindo os arquivos NetCDF4
# GPM Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06
# Período: 2001/01/01 00:00 UTC - 2020/12/31 23:30 UTC
# Período das estações meteorológicas: DJF, MAM, JJA, SON
print('3. Read of datasets')
ds_files = '/home/ronald/DJF/3B-HHR.*.nc4'
#ds_files = '/home/ronald/dados_imerg_AM/DJF/3B-HHR.*.nc4'
ds = xr.open_mfdataset(ds_files, combine = 'nested', concat_dim = 'time')
#print('Seleccionando a Área de estudo')
#ds = ds.sel(lon=slice(-75,-55), lat=slice(-10,3))"
print('4. Read dataset complete')
# --------------------------------------------------------------------------------------------------

# Criando uma nova dimensão coord de tempo <- hour_min
# A nova dimensão tem o formato HH:MM para fazer o groupby sobre essa dimensão
# e assim criar os composites para cada passo de tempo de 30 minutos (ou 0.5 hour)
print('5. Asignando uma nova dimensão de tempo HH:MM')
da = ds.assign_coords(hour_min = ds.time.dt.strftime('%H:%M'))
print('6. Terminou de criar a nova dimensão de tempo <- hour_min')

# Fazendo o groupby sobre a nova dimensão 'hour_min' que tem um formato HH:MM
print('7. Fazendo o groupby na dimensão -hour_min-') 
sdata = da.groupby('hour_min').mean('time')
print('8. Terminou de calcular os composites para cada passo de tempo e para cada pixel')
# ----------------------------------------------------------------------------------------------------

# Cobvertendo o xarray para DataFrame para fazer o cálculo dos parâmetros da 
# Análise harmônica
print('9. Convertendo o xarray para um DataFrame')
precip_df = sdata.to_dataframe().reset_index()
print('10. Fazendo um redondeo para 2 decimais e.g., x.ab <- (x:inteiro; a,b:decimais')
precip_df = precip_df.round({"lat":2, "lon":2})
print('11. Terminou de fazer o redondeo')

# Coletando os composites de cada passo de tempo por filas com o 'apply(np.array)'
print('12. Coletando os composites de cada paso de tempo em filas')
harm_group_df = precip_df.groupby(['lat','lon'])['precipitationCal'].apply(np.array).reset_index()
# -------------------------------------------------------------------------------------------------------

# Aplicando a função harmônica
# axis = 1 <- é para iterar por filas dentro do array 'precipitationCal' e não por colunas
print('13. Aplicando a função harmônica')
harm_group_df['harmonic'] = harm_group_df.apply(lambda x:harmonico(x['precipitationCal']), axis = 1)
print('14. Terminou de aplicar a função harmônica')

# Agora a dividir a coluna 'harmonic' para obter os parâmetros por separado
print('15. Dividindo a coulna -harmonic- para ter os parâmetros separados' )
harm_group_df['C1_24h'] = harm_group_df['harmonic'].apply(lambda x:x[0])
harm_group_df['C2_24h'] = harm_group_df['harmonic'].apply(lambda x:x[1])
harm_group_df['F1_UTC'] = harm_group_df['harmonic'].apply(lambda x:x[2])
harm_group_df['F2_UTC'] = harm_group_df['harmonic'].apply(lambda x:x[3])
harm_group_df['F2_12h_UTC'] = harm_group_df['harmonic'].apply(lambda x:x[4])
harm_group_df['ppmean'] = harm_group_df['harmonic'].apply(lambda x:x[5])
print('16. Colunas de amplitudes, fases e ppmean criadas')

# Removendo as colunas dos arrays 'precipitationCal' e 'harmonic'
print('17. Eliminação das colunas precip_mean e harmonic')
harm_group_df = harm_group_df.drop(harm_group_df.columns[[2,3]], axis = 'columns')
print('18. Colunas precipitationCal e harmonic removidas')
# Fazendo um redondeo dos números para 2 decimais e.g., x.ab <- (x: enteiro, a,b: decimais)
print('19. Fazendo o redondeo para dois decimais dos parâmetros harmicos')
harm_group_df = harm_group_df.round({"C1_24h":2,"C2_24h":2,"F1_UTC":2,"F2_UTC":2,"F2_12h_UTC":2,"ppmean":2})
print('20. Redondeo dos parâmetros harmônicos feito com sucesso')

# Fazendp a conversão de hora UTC para LST
print('21. Fazendo a conversão de hora UTC para LST')
harm_group_df['F1_LST'] = harm_group_df.apply(lambda x:LST(x['lon'],x['F1_UTC']), axis = 1)
harm_group_df['F2_LST'] = harm_group_df.apply(lambda x:LST(x['lon'],x['F2_UTC']), axis = 1)
harm_group_df['F2_12h_LST'] = harm_group_df.apply(lambda x:LST(x['lon'],x['F2_12h_UTC']), axis = 1)
print('22. Conversão de hora UTC para LST feita com sucesso')

# Removendo as colunas dos horários UTC 'F1_UTC', 'F2_UTC'
print('23. Removendo as colunas das fases em horário UTC')
harm_group_df = harm_group_df.drop(harm_group_df.columns[[4,5,6]], axis = 'columns')
print('24. Colunas de hora UTC removidas com sucesso')

# Ordenando os primeiros máximos do 2º harmônico
print('25. Função para ordenar os primeiros máximos do 2º harmônico')
def maior_12h(time):
    if time > 12:
        time = time - 12
    return time

# Ordenando os segundos máximo do 2º harmônico
print('26. Função para ordenar os segundos máximos do 2º harmônico')
def menor_12h(time):
    if time < 12:
        time = time + 12
    return time

print('27. Aplicando as funções de ordem dos horários dos 2º harmônicos')
harm_group_df['F2_LST'] = harm_group_df.apply(lambda x:maior_12h(x['F2_LST']), axis = 1)
harm_group_df['F2_12h_LST'] = harm_group_df.apply(lambda x:menor_12h(x['F2_12h_LST']), axis = 1)
print('28. Ordenamento das fases do 2º harmônico feito com sucesso')

# Fazendo um redondeo dos números para 2 decimais e.g., x.ab <- (x: enteiro, a,b: decimais)
print('29. Fazendo um redondeo dos números para 2 decimais das fases')
harm_group_df = harm_group_df.round({"F1_LST":2,"F2_LST":2,"F2_12h_LST":2})
print('30. Redondeo a duas decimais das colunas LST feito com sucesso')

# ---------------------------------------------------------------------------------------------------------------
# Transformando o df a xarray e asignando um Sist. Referência
print('31. Transformando o df a xarray e asignando um Sist. Referência')
harm_group_df.set_index(['lat','lon'], inplace = True)
harm_array = harm_group_df.to_xarray()
harm_array.rio.write_crs('epsg:4326', inplace = True)
print('32. Sistema de Referência asignado com sucesso')

# Escrevendo dados em um arquivo NetCDF novo
print('Escrevendo os dados em formato Netcdf para DJF')
harm_array.to_netcdf('diurnal_cycle_DJF.nc')
print('33. Arquivo NetCDF criado para DJF')



