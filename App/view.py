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


cont = {}

while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "w":
        print("\nInicializando....")
        C1 = input("inserte 1 para BST y 2 para RBT")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init(C1)

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
        print('Cantidad de fechas restrigadas: ', controller.sizeOmap(cont['dateIndex']))
        print('altura del dateIndex: ', controller.heightOmap(cont["dateIndex"]))
        print('Cantidad de Horas registradas: ', controller.sizeOmap(cont['timeIndex']))
        print('altura del TimeIndex: ', controller.heightOmap(cont["timeIndex"]))
        print('Cantidad de cordenadas registradas: ', cont["ZoneIndexLatLng"]['num_zones'])
        print('altura del IndexLat: ', controller.heightOmap(cont["ZoneIndexLatLng"]['DoubleMap']))

    elif int(inputs[0]) == 1:
        fecha = input("Ingrese la fecha a consultar\n")
        t1 = perf_counter()
        print("\nBuscando accidentes para la fecha: ", fecha)
        dateEntry = controller.requirement1(cont, fecha)
        pairs1 = [('accidentes', 'value')]
        print('|| Accidentes por severidad ||\n')
        PrintListEntry(dateEntry['list'], pairs1)
        print('total de accidentes', dateEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 2:
        fecha = input("Ingrese la fecha posterior a la busqueda: \n")
        t1 = perf_counter()
        print("\nBuscando accidentes antes de la fecha: ", fecha)
        w = controller.requirement2(cont, fecha)
        print('|| fecha con mas accidentes antes de la fecha ingresada ||\n')
        reference2 = ['fecha con mas accidentes', 'numero maximo de accidentes', 'total accidentes']
        PrintMaxEntry(w, reference2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en un rango de fechas: \n")
        fecha1 = input("fecha 1")
        fecha2 = input('fecha 2')
        t1 = perf_counter()
        w = controller.requirement3(cont, fecha1, fecha2)
        print('|| Severidad mas frecuente antes de la fecha ||\n')
        reference2 = ['Severidad mas comun', 'numero maximo de accidentes', 'total accidentes']
        PrintMaxEntry(w, reference2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 4:
        fecha1 = input("fecha1")
        fecha2 = input('fecha2')
        t1 = perf_counter()
        print("\nBuscando accidentes en un rango de fechas: \n")
        w = controller.requirement4(cont, fecha1, fecha2)
        print('para el rango de fechas: ', fecha1, 'a', fecha2)
        reference2_1 = ['Estado', 'accidentes']
        reference2_2 = ['Fecha', 'accidentes']
        print('|| Estado con mas accidentes en el rango de fechas ||')
        PrintMaxEntry(w['mState'], reference2_1)
        print('|| Fecha con mas accidentes en el rango de fechas ||')
        PrintMaxEntry(w['mKey'], reference2_2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 5:
        hora1 = input("time1: ")
        hora2 = input('time2: ')
        t1 = perf_counter()
        print("\nBuscando crimenes en un rango de horas: \n")
        SeverityEntry = controller.requirement5(cont, hora1, hora2)
        pairs5 = [('accidentes', 'value'), ('porcentaje', 'percent')]
        print('|| Accidentes por severidad ||\n')
        PrintListEntry(SeverityEntry['list'], pairs5)
        print('total de accidentes', SeverityEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 6:
        lat = input("latitud: ")
        lng = input('longitud: ')
        distancia = input('distancia: ')
        pairs6 = [('accidentes', 'value')]
        t1 = perf_counter()
        print("\nBuscando accidentes en la zona ingresada: ")
        weekdayEntry = controller.requirement6(cont, lat, lng, distancia)
        print('|| Accidentes por dia de la semana||\n')
        PrintListEntry(weekdayEntry['list'], pairs6)
        print('total de accidentes :', weekdayEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    else:
        break
