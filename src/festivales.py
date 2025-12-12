from collections import Counter, defaultdict
from typing import Dict, NamedTuple
from datetime import time, date, datetime
import csv


Artista = NamedTuple("Artista",     
                        [("nombre", str), 
                        ("hora_comienzo", time), 
                        ("cache", int)])

Festival = NamedTuple("Festival", 
                        [("nombre", str),
                        ("fecha_comienzo", date),
                        ("fecha_fin", date),
                        ("estado", str),                      
                        ("precio", float),
                        ("entradas_vendidas", int),
                        ("artistas", list[Artista]),
                        ("top", bool)
                    ])

def lee_festivales(archivo:str) -> list[Festival]:
    res = []
    with open(archivo, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for nombre, fecha_ini, fecha_fin, estado, precio, entradas, artistas, top in lector: 
            fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            precio = float(precio)
            entradas = int(entradas)
            artistas = parsea_artistas(artistas)
            top = parsea_booleano(top)
            tupla = Festival(nombre, fecha_ini, fecha_fin, estado, precio, entradas, artistas, top)
            res.append(tupla)
    return sorted(res, key= lambda x:x.fecha_comienzo)

def parsea_artistas(cadena: str) -> list[Artista]:
    # The Strokes_20:00_500-Radiohead_21:00_700-Kendrick Lamar_22:30_800-Tame Impala_00:00_750-Billie Eilish_01:30_850
    lista_artistas = []
    for artista in cadena.split('-'):
        artista = parsea_artista(artista)
        lista_artistas.append(artista)
    return lista_artistas

def parsea_artista(cadena:str) -> Artista:
    # The Strokes_20:00_500
    # Radiohead_21:00_700
    # Kendrick Lamar_22:30_800
    nombre, hora, cache = cadena.split('_')
    hora = datetime.strptime(hora, '%H:%M').time()
    return Artista(nombre, hora, int(cache))

def parsea_booleano(cadena: str) -> bool:
    res = None
    if cadena == 'sí':
        res = True
    elif cadena == 'no':
        res = False
    return res


def total_facturado(festivales: list[Festival], fecha_ini: date | None = None, fecha_fin: date | None= None) -> float:
    total = 0
    for f in festivales:
        if f.estado == 'CELEBRADO' and fecha_en_rango(f, fecha_ini, fecha_fin):
            total += f.precio * f.entradas_vendidas
    return total


def fecha_en_rango(f: Festival, fecha_ini: date | None = None, fecha_fin: date | None = None) -> bool:
    if (fecha_ini is None or f.fecha_comienzo >= fecha_ini) and \
    (fecha_fin is None or f.fecha_fin <= fecha_fin): 
        return True
    else: 
        return False
    

def artista_top(festivales: list[Festival]) -> tuple[int, str]:
    artistas_fest = Counter(a.nombre for f in festivales for a in f.artistas if f.estado == 'CELEBRADO')
    artista_mas_fest = artistas_fest.most_common(1)[0]
    return (artista_mas_fest[1], artista_mas_fest[0])

'''
dicc = defaultdict(int)
for f in festivales:
    if f.estado == 'CELEBRADO':
        for a in f.artistas:
            dicc[a.nombre] += 1
artistas_fest = max(res.items(), key= lambda x:x[1])
return (artista_fest[1], artista_fest[0])

'''


def mes_mayor_beneficio_medio(festivales: list[Festival]) -> str:
    dicc = defaultdict(list)
    for f in festivales:
        dicc[f.fecha_comienzo.month].append(calcular_facturacion(f))
    
    for mes, beneficios in dicc.items():
        dicc[mes] = sum(beneficios)/len(beneficios)
    # dicc = {mes: sum(beneficios) / len(beneficios) for mes, beneficios in dicc.items()}

    mes = max(dicc, key = dicc.get)
    return mes_str(mes)


def mes_str(mes:int) -> str:
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
             'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return meses[mes-1]



def calcular_facturacion(f: Festival) -> float:
    gastos = sum(a.cache*1000 for a in f.artistas) #*1000 pq es cache en millones
    return f.precio * f.entradas_vendidas - gastos


def artistas_comunes(festivales: list[Festival], festi1: str, festi2:str) -> list[str]:

    '''
    artistas_f1 = None
    artistas_f2 = None

    for f in festivales:
        if f.nombre == fest1:
            artistasf1 = set(f.artistas)
        elif f.nombre == fest2:
            artistas_f2 = set(f.artistas)
        if 
    '''


    f1 = {a.nombre for f in festivales for a in f.artistas if f.nombre == festi1}
    f2 = {a.nombre for f in festivales for a in f.artistas if f.nombre == festi2}
    return list(f1.intersection(f2))


def festivales_top_calidad_por_duracion(festivales: list[Festival], n: int=3) -> Dict[int, list[str]]:
    '''
    Cada festival tiene una duración de entre 2 y 8 días. 
    Implemente una función que, recibiendo una lista de tuplas de tipo Festival, y un número n cuyo valor 
    por defecto será 3, devuelva un diccionario en el que las claves son las duraciones de los festivales, 
    y los valores listas con los nombres de los n festivales de más calidad (ordenados de más a menos calidad). 
    La calidad de un festival viene dada por el ratio entre entradas vendidas y número de artistas participantes
    en el festival. Cuanto más alto es este ratio, más calidad tiene el festival.
    '''
    dicc = defaultdict(defaultdict)
    for f in festivales:
        duracion = (f.fecha_fin - f.fecha_comienzo).days
        ratio = f.entradas_vendidas - len(f.artistas)
        dicc[duracion].update({f.nombre:ratio})
    

    for duracion, dicc_fest in dicc.items():
        dicc[duracion] = sorted(dicc_fest, key = dicc_fest.get, reverse = True)[:n] #get devuelve la clave 

    return dicc


def variacion_mensual_asistentes(festivales:list[Festival])->list[tuple[str,int]]:
    '''
    variacion_mensual_asistentes: recibe una lista de tuplas de tipo Festival y devuelve una lista de tuplas 
    con cada mes y la variación que asistente de un mes repecto al anterior a los festivales. 
    Se considerará el mes de la fecha de comienzo del festival y que cada entrada vendida se corresponde con un asistente.
    '''

    pass