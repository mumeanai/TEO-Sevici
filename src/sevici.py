#a traves de este proyecto veremos: lambda, tipado, generadores

from coordenadas import *
from typing import NamedTuple
import csv

Estacion = NamedTuple('Estacion', [
    ("nombre",str)
    ("bornetas", int)
    ("bornetas_vacias", int)
    ("bicis_disponibles", int)
    ("ubicacion", Coordenadas)
    ])

#ejemplo de uso de una tupla Estacion 

#tupla = Estacion("Reina Mercedes", 20,10,10, Coordenadas(1.0, 2.0))

def lee_estaciones(ruta: str)-> list[Estacion]: 
    #la funcion recibe una cadena de texto y devuelve una lista, cuyos elementos son tupla
    '''
    Recibe una ruta de tipo str, y devuelve una lista de tuplas de 
    tipo Estacion. La función lee un fichero csv de la ruta indicada
    y devuelve la información en la lista
    '''
    
    with open(ruta, enconding = "utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        res = []
        
        for name,slots,empty_slots,free_bikes,latitude,longitude in lector:
            slots = int(slots)
            empty_slots = int(empty_slots)
            free_bikes = int(free_bikes)
            latitude = float(latitude)
            longitud = float(longitud)
            ubicacion = Coordenadas(latitude, longitud)
            tupla = Estacion(name,slots,empty_slots,free_bikes,ubicacion)
            res.append(tupla)
        return res
    
def estaciones_bicis_libres(estaciones: list[Estacion], k:int = 5) -> list[()]:
    # el hecho de que ponga el valor de k, significa que si al llamar la funcion no le doy un valor, tendrá por defecte este
    
    ''' Estaciones que tienen bicicletas libres
    
    ENTRADA: 
      :param estaciones: lista de estaciones disponibles 
      :type estaciones: [Estacion(str, int, int, int, Coordenadas(float, float))]
      :param k: número mínimo requerido de bicicletas
      :type k: int
    SALIDA: 
      :return: lista de estaciones seleccionadas
      :rtype: [(int, str)] 
    
    Toma como entrada una lista de estaciones y un número k.
    Crea una lista formada por tuplas (número de bicicletas libres, nombre)
    de las estaciones que tienen al menos k bicicletas libres. La lista
    estará ordenada por el número de bicicletas libres.
    '''
    res = []
    for e in estaciones: 
        if e.bicis_disponibles >= k:
            res.append((e.bicis_disponibles, e.nombre))
    res.sort(reverse = True) #ordenamos la lista de más a menos bicis disponibles
    return #no lo puedo poner antes, a la izquierda de res.sort(), dado que eso devolveria none

def estaciones_bicis_libres_2(estaciones: list[Estacion], k: int = 5 ):
    '''Versión usando GENERADOR'''
    #sintaxis de un generador
    #EXPRESION_GENERADORA for elem in secuencia if CONDICION
    res = [ (e.bicis_disponibles, e.nombre) for e in estaciones if e.bicis_disponibles >= k]
    #si en vez de una lista quiero un conjunto, basta con cambiar los conrchetes por llaves

def total_bicis_estaciones(estaciones:list[Estacion], nombre_calle: str ) -> int:
    '''
    Devuelve cuántas bicis hay en todas las estadiones cuyo nombre contenga nombre_calle.
    '''

    suma=0
    for e in estaciones:
        if nombre_calle in e.nombre:
            suma += e.bicis_dispoonibles
            
    suma = sum(e.bicis_disponibles for e in estaciones if nombre_calle in e.nombre)
#uso util de un generador

def estaciones_cercanas(estaciones:list[Estacion], coordenadas: Coordenadas, k:int =5) -> list[tuple[float, int, int]]:
    ''' Estaciones cercanas a un punto dado
    
    ENTRADA: 
      :param estaciones: lista de estaciones disponibles
      :type estaciones: [Estacion(str, int, int, int, Coordenadas(float, float))]
      :param coordenadas: coordenadas formada por la latitud y la longitud de un punto
      :type coordenadas: Coordenadas(float, float)
      :param k: número de estaciones cercanas a calcular 
      :type k: int
    SALIDA: 
      :return: Una lista de tuplas con la distancia, nombre y bicicletas libres de las estaciones seleccionadas 
      :rtype: [(float, str, int)] 
    
    Toma como entrada una lista de estaciones,  las coordenadas de  un punto y
    un valor k.
    Crea una lista formada por tuplas (distancia, nombre de estación, bicicletas libres)
    con las k estaciones con bicicletas libres más cercanas al punto dado, ordenadas por
    su distancia a las coordenadas dadas como parámetro.
    '''
    res = []
    
    for e in estaciones:
        if e.bicis_disponibles != 0:
            distancia = calcula_distancia(e.coordenadas, coordenadas)
            res.append((distancia, e.nombre, e.bicis_disponibles))
    res.sort() #se esta ordenando de menor a mayor segun distacia
    #res.sort(key =lambda t:t[2]) si pongo esto, estoy ordenando segun los valores del segundo elemento de la tupla, bicis_disponibles
    #res.sort(key = lambda t:t[2], t[0])  asi sigue ordenando por bicis_disponibles, pero si este valor es igual en dos tuplas, ordeno segun este segundo elemento
    return res[:k]

#intentemos definir la funcion en una sola línea
def estaciones_cercanas(estaciones:list[Estacion], coordenadas: Coordenadas, k:int =5) -> list[tuple[float, int, int]]:
    
    return sorted(
        #GENERADOR
        ## 1.- expresion generadora
        (calcula_distancia(e.ubicacion, coordenadas), e.nombre, e.bicis_disponibles)
        ## 2.- bucle con if
        for e in estaciones if e.bicis_disponibles != 0
        ## FIN GENERADOR
        )[k:]
    
def estacion_con_mas_bicis(estaciones: list[Estacion], coordenadas: Coordenadas, umbral: float) -> Estacion:
    '''
    Devuelve la estación con más bicis disponibles de entre 
    las que están a menos distacia que "umbral" de "coordenadas".
    '''
    filtrado = []
    for e in estaciones:
        if calcula_distancia(e.ubicacion, coordenadas) < umbral:
            filtrado.append(e)
    
    return max(estaciones, key = lambda e: e.bicis_disponibles) 
#de todas las estaciones disponibles, cojo las que tienen bicis disponibles

def estacion_con_mas_bicis_2(estaciones: list[Estacion], coordenadas: Coordenadas, umbral: float) -> Estacion:
    return max(
        (e for e in estaciones if calcula_distancia((e.ubicacion, coordenadas) < umbral)),
        key = lambda e: e.bicis_disponibles
    )
    
#esta segunda opcion es más eficiente porque no se recquiere crear una copia de la lista para hacer el filtrado