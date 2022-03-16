'''

Este software é utilizado para fazer a Análise harmônica segundo a metodología de 
Wilks (2011). É definida uma função harmônica com o objetivo de calcular os dois
primeiros harmônicos para analisar as oscilações diurnas (oscilações de 24 h, 
mediante o 1º harmônico) e oscilações semidiurnas (oscilações de 12 h, meduante
o 2º harmônico). A função vai retornar como resultados os parâmetros de: 
Amplitude e fase para os dois harmônicos

Autor: Ronald Guiuseppi Ramírez Nina
Magister Student at Instituto de Astronomia, Geofísica e Ciências Atmosféricas
Universidade de São Paulo

'''

# Importando livrarias
import pandas as pd
import numpy as np
from scipy.signal import *
import math

# Definindo a função harmonica

def harmonico(dados):

    n = 48    # Tamanho da amostra
    k1 = 1    # Representa o harmônico 1º
    k2 = 2    # Representa o hârmonico 2º
    t = np.arange(1,n+1,1) # Índice do tempo
    ppmean = np.mean(dados)  # pp media diurna das 24 h

    # Calculando os harmônicos 1º e 2º
    # Para o harmônico 1 
    FA1 = dados * np.cos(2*np.pi*t*k1/n)
    FB1 = dados * np.sin(2*np.pi*t*k1/n)
    # Para o harmônico 2
    FA2 = dados * np.cos(2*np.pi*t*k2/n)
    FB2 = dados * np.sin(2*np.pi*t*k2/n)

    # Calculando os coeficientes A1, A2, B1, B2
    A1 = (2/n) * np.sum(FA1)
    A2 = (2/n) * np.sum(FA2)
    B1 = (2/n) * np.sum(FB1)
    B2 = (2/n) * np.sum(FB2)

    # Calculando as amplitudes para os harmônicos 1º e 2º
    C1 = (A1**2 + B1**2)**0.5
    C2 = (A2**2 + B2**2)**0.5

    # Calculando as amplitudes normalizadas dos harmônicos 1º e 2º
    C1_24h = C1 / ppmean
    C2_24h = C2 / ppmean

    # Redondeando para duas decimais os parâmetros de A1,A2,B1,B2
    # Eliminando possíveis resultados de -0.00
    A1 = round(A1,4)
    if A1 == -0.0000:
        A1 = abs(A1)

    A2 = round(A2,4)
    if A2 == -0.0000:
        A2 = abs(A2)

    B1 = round(B1,4)
    if B1 == -0.0000:
        B1 = abs(B1)

    B2 = round(B2,4)
    if B2 == -0.0000:
        B2 = abs(B2)

    # Calculando a fase para o 1º harmônico
    if A1 > 0:
        fase1 = np.arctan(B1/A1)

    elif A1 < 0:
        if np.arctan(B1/A1) < np.pi:
            fase1 = np.arctan(B1/A1) + np.pi
        else:
            fase1 = np.arctan(B1/A1) - np.pi

    elif A1 == 0.0000:
        fase1 = np.pi/2
     
    # Fazendo que a fase esteja no dominio de [0 ; 2*np.pi]
    # Considerando que um ângulo negativo tem sentido horário
    # Considerando que um ângulo positivo tem sentido anti-horário
    # Então, o equivalente de -320º é o mesmo que fazer: 360º - abs(-320º) = 40º
    # Se o ângulo é maior que 2*np.pi (por exemplo 400º), então: 400º - 360 = 40º
     
    if fase1 < 0:
        fase1 = 2*np.pi - abs(fase1)
    elif fase1 > 2*np.pi:
        fase1 = fase1 - 2*np.pi

    # Calculando a fase para o 2º harmônico
    if A2 > 0:
        fase2 = np.arctan(B2/A2)

    elif A2 < 0:
        if np.arctan(B2/A2) < np.pi:
            fase2 = np.arctan(B2/A2) + np.pi
        else:
            fase2 = np.arctan(B2/A2) - np.pi

    elif A2 == 0.0000:
        fase2 = np.pi/2
    
    # Fazendo que a fase esteja no dominio de [0 ; 2*np.pi]
    # Considerando que um ângulo negativo tem sentido horário
    # Considerando que um ângulo positivo tem sentido anti-horário
    # Então, o equivalente de -320º é o mesmo que fazer: 360º - abs(-320º) = 40º
    # Se o ângulo é maior que 2*np.pi (por exemplo 400º), então: 400º - 360 = 40º
     
    if fase2 < 0:
        fase2 = 2*np.pi - abs(fase2)
    elif fase2 > 2*np.pi:
        fase2 = fase2 - 2*np.pi

    # Calculando as fases em unidades de tempo (UTC)

    # Para o 1º harmônico
    F1_UTC = (fase1 * 48 / (2 * np.pi *k1)) / 2
    
    # Para o 2º harmônico
    F2_UTC = (fase2 * 48 / (2 * np.pi * k2)) / 2

    F2_12UTC = F2_UTC + 12

    return C1_24h, C2_24h, F1_UTC, F2_UTC, F2_12UTC, ppmean



