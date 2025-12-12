from festivales import *

def test_lee_festivales(datos):
    print('test_lee_festivales')
    print(f'Registros leidos: {len(datos)}')
    print('Los 3 primeros:')
    print('\n'. join(str(fest) for fest in datos[:3]))

def test_total_facturado(datos):
    print('\ntest_total_facturado')
    total = total_facturado(datos)
    print(f'Entre None y None el total es {total}')
    
    fecha_fin = date(2024, 6, 15)
    total = total_facturado(datos, fecha_fin=fecha_fin)
    print(f'Entre None y {fecha_fin} el total es: {total}')

    fecha_ini = date(2024, 6, 15)
    total = total_facturado(datos, fecha_ini)
    print(f'Entre {fecha_ini} y None el total es: {total}')

    fecha_ini = date(2024,6,1)
    fecha_fin = date(2024, 6, 15)
    total = total_facturado(datos, fecha_ini, fecha_fin)
    print(f'Entre {fecha_ini} y {fecha_ini} el total es: {total}')

def test_artista_top(datos):
    print('\ntest_artista_top')
    print(f'El artista que ha actuado en más festivales es {artista_top(datos)}')

def test_mes_mayor_beneficio_medio(datos):
    print('\ntest_mayor_beneficio')
    print(f'El mes de mayor beneficio medio es: {mes_mayor_beneficio_medio(datos)}')


def test_artistas_comunes(datos):
    print('\ntest_artistas_comunes')
    f1 = 'Creamfields'
    f2 = 'Tomorrowland'
    print(f'Los artistas comunes entre {f1} y {f2} son: {artistas_comunes(datos,f1,f2)}')
    
    f1 = 'Primavera Sound'
    f2 = 'Coachella'
    print(f'Los artistas comunes entre {f1} y {f2} son: {artistas_comunes(datos,f1,f2)}')

    f1 = 'Iconica Fest'
    f2 = 'Primavera Sound'
    print(f'Los artistas comunes entre {f1} y {f2} son: {artistas_comunes(datos,f1,f2)}')

def test_festivales_top_calidad_por_duracion(datos):
    print('\ntest_festivales_top_calidad_por_duracion')
    print('Para n = 1, los festivales top son:')
    resultado = festivales_top_calidad_por_duracion(datos, 1)
    for duracion in resultado:
        print(f'{duracion} --> {resultado[duracion]}')



def main():
    festivales = lee_festivales('data/festivales.csv')   #el './' significa que 'data/festivales.csv' está en el directorio en el que estoy
    test_lee_festivales(festivales)
    test_total_facturado(festivales)
    test_artista_top(festivales)
    test_mes_mayor_beneficio_medio(festivales)
    test_artistas_comunes(festivales)
    test_festivales_top_calidad_por_duracion(festivales)


if __name__ == '__main__':
    main()