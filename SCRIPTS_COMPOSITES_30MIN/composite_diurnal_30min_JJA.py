'''
Versão 1

Código em Python para calcular as médias horárias (composites com dt = 30 min) 
dos dados de precipitação. A análise será feita para o estudo do "Ciclo
diurno da precipitação na Bacia Amazônica" para o período de JJA.

Autor: Ronald Guiuseppi Ramírez Nina
Estudante de Mestrado 
Departamento de Ciências Atmosféricas IAG - USP
Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Paulo

'''

# Importando livrarias
print('Rodando código para o período de JJA')

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

print('2. End to read packages')
# -------------------------------------------------------------------------------------------------

# Abrindo os arquivos NetCDF4
# GPM Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06
# Período: 2001/01/01 00:00 UTC - 2020/12/31 23:30 UTC
# Período das estações meteorológicas: DJF, MAM, JJA, SON
print('3. Read of datasets')
ds_files = '/home/ronald/JJA/3B-HHR.*.nc4'
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

# Escrevendo dados em um arquivo NetCDF novo
print('Escrevendo os dados em formato Netcdf para JJA')
sdata.to_netcdf('composite_diurnal_30min_JJA.nc')
print('9. Arquivo NetCDF criado para JJA')



