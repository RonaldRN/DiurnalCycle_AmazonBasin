'''

Este software é utilizado para fazer a conversão do horário Universal Time Coordinate (UTC) 
para o Local Solar Time (LST)

LST(h) = UTC(h)  +   longitude(º)   (h)
                    -------------- 
                         15º

- LST(h) : Local Solar Time (unidades em horas)
- UTC(h) : Universal Time Coordinate (unidades em horas)
- longitude(º) : Longitude considerando -180º até +180º (unidades º)

Autor: Ronald Guiuseppi Ramírez Nina
Magister Student at Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Paulo

'''

def LST(lon,utc):

    t_lst = utc + lon/15

    if t_lst < 0:
        t_lst = 24 + t_lst
    
    return t_lst