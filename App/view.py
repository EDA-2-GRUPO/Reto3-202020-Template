"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import sys
import config
from DISClib.ADT.list import size as lts
from App import controller
from time import perf_counter
from DISClib.DataStructures import listiterator as it

assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


dict_files = {'1': 'us_accidents_dis_2016.csv', '2': 'us_accidents_dis_2017.csv',
              '3': "us_accidents_dis_2018.csv", '4': "us_accidents_dis_2019.csv"}


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("w- Inicializar Analizador")
    print("q- Cargar información de accidentes")
    print("1- accidentes en una fecha")
    print("2- accidentes anteriores a una fecha")
    print("3- accidentes en un rango de fechas, por severidad")
    print("4- el estado con mas accidentes (en rango de fechas)")
    print("5- accidentes por rango de horas")
    print("6- zona geográfica mas accidentada")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""

"""
Funciones de Printeo
"""


def PrintListEntry(g, pairs):
    iterator = it.newIterator(g)
    for _ in range(lts(g)):
        el = it.next(iterator)
        text = '[ ' + str(el['key']) + ' ]   '
        for pair in pairs:
            text += pair[0] + " : " + str(el[pair[1]]) + "  "
        print(text)


def PrintMaxEntry(entry, reference):
    i = 0
    for v in entry.values():
        print(reference[i], ':', v)
        i += 1


"""
Funciones de Printeo
"""


def inicializar():
    print("\nInicializando....")
    C1 = input("inserte 1 para BST y 2 para RBT")
    # cont es el controlador que se usará de acá en adelante
    cont_i = controller.init(C1)
    return cont_i


cont = inicializar()
dateIndex = cont.get('dateIndex')
timeIndex = cont.get('timeIndex')
zoneIndex = cont.get("ZoneIndexLatLng")
cargo = False

while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "w":
        del cont
        cont = inicializar()
        cargo = False

    elif inputs[0] == "q":
        list_files = []
        print("\nCargando información de accidentes ....")
        print(' En formato 1,2,3,4')
        C2 = input('ingrese los años 2016: 1, 2017: 2, 2018: 3, 2019: 4')
        t1 = perf_counter()
        for nm in C2.split(','):
            list_files.append(dict_files[nm])
        controller.loadData(cont, list_files)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
        cargo = True
        print('Cantidad de fechas restrigadas: ', controller.sizeOmap(dateIndex))
        print('altura del dateIndex: ', controller.heightOmap(dateIndex))
        print('Cantidad de Horas registradas: ', controller.sizeOmap(timeIndex))
        print('altura del TimeIndex: ', controller.heightOmap(timeIndex))
        print('Cantidad de cordenadas registradas: ', zoneIndex['num_zones'])
        print('altura del primer Omap Latitude: ', controller.heightOmap(zoneIndex['DoubleMap']))

    elif int(inputs[0]) == 1:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(dateIndex) == 0:
            print('no se ha cargado el dateIndex')
            continue
        else:
            fecha = input("Ingrese la fecha a consultar\n")
            t1 = perf_counter()
            print('...')
            dateEntry = controller.requirement1(dateIndex, fecha)
            if dateEntry is None:
                print('No se encontro la fecha')
                continue
            pairs1 = [('accidentes', 'value')]
            print('para la fecha', fecha, '\n')
            print('|| Accidentes por severidad ||')
            PrintListEntry(dateEntry['list'], pairs1)
            print('total de accidentes', dateEntry['total'])
            print('')
            t2 = perf_counter()
            print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 2:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(dateIndex) == 0:
            print('no se ha cargado el dateIndex')
            continue
        else:
            fecha = input("Ingrese la fecha posterior a la busqueda: \n")
            t1 = perf_counter()
            print('...')
            maxSeverity = controller.requirement2(dateIndex, fecha)
            print('para antes de la fecha: ', fecha, '\n')
            print('|| fecha con mas accidentes ||')
            reference2 = ['fecha', 'numero de accidentes', 'total accidentes']
            PrintMaxEntry(maxSeverity, reference2)
            print('')
            t2 = perf_counter()
            print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 3:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(dateIndex) == 0:
            print('no se ha cargado el dateIndex')
            continue
        else:
            fecha1 = input('fecha 1\n')
            fecha2 = input('fecha 2\n')
            t1 = perf_counter()
            print('...')
            maxSeverity = controller.requirement3(dateIndex, fecha1, fecha2)
            print('para el rango de fechas: ', fecha1, 'a', fecha2, '\n')
            print('|| Severidad mas frecuente ||')
            reference2 = ['Severidad', 'numero de accidentes', 'total accidentes']
            PrintMaxEntry(maxSeverity, reference2)
            t2 = perf_counter()
            print('')
            print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 4:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(dateIndex) == 0:
            print('no se ha cargado el dateIndex')
            continue
        else:
            fecha1 = input("fecha1")
            fecha2 = input('fecha2')
            t1 = perf_counter()
            print('...')
            maxStateAndDate = controller.requirement4(dateIndex, fecha1, fecha2)
            print('para el rango de fechas: ', fecha1, 'a', fecha2, '\n')
            reference2_1 = ['Estado', 'accidentes']
            reference2_2 = ['Fecha', 'accidentes']
            print('|| Estado con mas accidentes ||')
            PrintMaxEntry(maxStateAndDate['mState'], reference2_1)
            print('|| Fecha con mas accidentes ||')
            PrintMaxEntry(maxStateAndDate['mKey'], reference2_2)
            print('')
            t2 = perf_counter()
            print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 5:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(timeIndex) == 0:
            print('no se ha cargado el timeIndex')
            continue
        else:
            hora1 = controller.proxyTime(input("time1: "))
            hora2 = controller.proxyTime(input('time2: '))
            pairs5 = [('accidentes', 'value'), ('porcentaje', 'percent')]
            t1 = perf_counter()
            print('...')
            SeverityEntry = controller.requirement5(timeIndex, hora1, hora2)
            print('para el rango de horas: ', hora1, 'a', hora2, '\n')
            print('|| Accidentes por severidad ||')
            PrintListEntry(SeverityEntry['list'], pairs5)
            print('total de accidentes', SeverityEntry['total'])
            t2 = perf_counter()
            print('')
            print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 6:
        if not cargo:
            print('necesita cargar los datos')
            continue
        elif controller.sizeOmap(zoneIndex['DoubleMap']) == 0:
            print('no se ha cargado el zoneIndex')
            continue
        else:
            lat = input("latitud: ")
            lng = input('longitud: ')
            distancia = input('distancia: ')
            pairs6 = [('accidentes', 'value')]
            t1 = perf_counter()
            print("\nBuscando accidentes en la zona ingresada: \n")
            weekdayEntry = controller.requirement6(zoneIndex['DoubleMap'], lat, lng, distancia)
            print('|| Accidentes por dia de la semana||')
            PrintListEntry(weekdayEntry['list'], pairs6)
            print('total de accidentes :', weekdayEntry['total'])
            t2 = perf_counter()
            print('')
            print("tiempo de carga:", t2 - t1)
    else:
        break
    input('presione cualquier tecla para continuar')
