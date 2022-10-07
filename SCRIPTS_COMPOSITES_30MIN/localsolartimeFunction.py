'''
#
# Este código é utilizado para fazer a conversão do horário Universal Time Coordinate (UTC) 
# para o formato de Local Solar Time (LST)
#
# LST(h) = UTC(h)  +   longitude(º)   (h)
#                     -------------- 
#                          15º
#
# - LST(h) : Local Solar Time (unidades em horas)
# - UTC(h) : Universal Time Coordinate (unidades em horas)
# - longitude(º) : Longitude considerando -180º até +180º (unidades º)
#
# Author: Ronald Guiuseppi Ramírez Nina
# e-mail: ronald.ramirez.nina@usp.br / ronald.ramirez.nina@gmail.com
# Estudante de Mestrado
# Departamento de Ciências Atmosféricas IAG - USP
# Instituto de Astronomia, Geofísica e Ciências Atmosféricas
# Universidade de São Pauo
#
'''

def LST(lon,utc):
    
    # INPUTS:
    # - lon: longitude (º)
    # utc: horário em formato UTC
    #
    # OUTPUTS:
    # - t_lst: horário no formato Local Solar Time

    t_lst = utc + lon/15

    if t_lst < 0:
        t_lst = 24 + t_lst
    
    return t_lst