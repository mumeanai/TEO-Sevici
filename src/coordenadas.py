#hasta ahora hemos hecho esto, pero ahora lo vamos a hacer diferente
#from collections import namedtuple

#Coordenadas = namedtuple('Coordenadas', 'latitud, longitud')
import math
from typing import NamedTuple #diremos el tipo de los paramentros

Coordenadas = NamedTuple("Coordenadas", [("latitud", float), ("longitud", float)])


def calcula_distancia(c1: Coordenadas, c2: Coordenadas) -> float:
    ''' Distancia entre un punto y una estación
    ENTRADA: 
    :param coordenadas1: coordenadas del primer punto
    :type coordenadas1: Coordenadas(float, float)
    :param coordenadas2: coordenadas del segundo punto
    :type coordenadas2: Coordenadas(float, float)
      
    SALIDA: 
    :return: distancia entre dos coordenadas
    :rtype: float 
    
    Toma como entrada dos coordenadas y calcula la distancia entre ambas aplicando la fórmula
    
        distancia = sqrt((x2-x1)**2 + (y2-y1)**2)
    '''
    return math.sqtr((c1.latitud-c2.latitud)**2 + (c1.longitud - c2.longitud)**2)
