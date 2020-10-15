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
from DISClib.DataStructures import orderedmapstructure as om

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


crimefile = 'us_accidents_dis_2016.csv'
crimefile2 = 'us_accidents_dis_2017.csv'
crimefile3 = 'us_accidents_dis_2018.csv'
crimefile4 = "us_accidents_dis_2019.csv"


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("w- Inicializar Analizador")
    print("q- Cargar información de accidentes")
    print("1- Requerimiento 1")
    print("2- Requerimiento 2")
    print("3- Requerimiento 3")
    print("4- Requerimiento 4")
    print("5- Requerimiento 5")
    print("6- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")


def Print1(g, pairs):
    iterator = it.newIterator(g)
    for _ in range(lts(g)):
        el = it.next(iterator)
        text = ""
        for pair in pairs:
            text += pair[0] + " : " + str(el[pair[1]]) + "  "
        print(text)


"""
Menu principal
"""


def Print2(entry, reference):
    for v in entry.values():
        print(reference, ':', str(v))
    pass


while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "w":
        print("\nInicializando....")
        C1 = input("inserte 1 para BST y 2 para RBT")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init(C1)
        
    elif inputs[0] == "q":
        print("\nCargando información de accidentes ....\n")
        archivos = input("1=2016, 2=2017,3=2018,4=2019\n(si quiere más de uno dijiteel numero separado por coma)\nEj: 1,2 \n")
        t1 = perf_counter()
        controller.loadData(cont, crimefile, crimefile2,crimefile3,crimefile4,archivos)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
        print(om.height(cont["dateIndex"]))
        print(om.size(cont["dateIndex"]))

    elif int(inputs[0]) == 1:
        fecha = input("Ingrese la fecha a consultar\n")
        t1 = perf_counter()
        print("\nBuscando accidentes para la fecha: ", )
        dateEntry = controller.requirement1(cont, fecha)
        pairs1 = [('Severity', 'key'), ('accidentes', 'value')]
        Print1(dateEntry['list'], pairs1)
        print('total de accidentes', dateEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 2:
        fecha = input("Ingrese la fecha posterior a la busqueda: \n")
        t1 = perf_counter()
        print("\nBuscando accidentes antes de la fecha: ", fecha)
        w = controller.requirement2(cont, fecha)
        reference2 = ['fecha con mas accidentes', 'numero maximo de accidentes', 'total accidentes']
        Print2(w, reference2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en un rango de fechas: \n")
        fecha1 = input("fecha 1")
        fecha2 = input('fecha 2')
        t1 = perf_counter()
        w = controller.requirement3(cont, fecha1, fecha2)
        reference2 = ['tipo mas comun', 'numero maximo de accidentes', 'total accidentes']
        Print2(w, reference2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 4:
        fecha1 = input("fecha1")
        fecha2 = input('fecha2')
        t1 = perf_counter()
        print("\nBuscando accidentes en un rango de fechas: \n")
        w = controller.requirement4(cont, fecha1, fecha2)
        print('para el rango de fechas: ', fecha1, 'a', fecha2)
        reference2 = ['Estado con mas accidentes', 'numero maximo de accidentes', 'total accidentes']
        Print2(w, reference2)
        # Printlistafinal(w)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 5:
        hora1 = input("time1: ")
        hora2 = input('time2: ')
        t1 = perf_counter()
        print("\nBuscando crimenes en un rango de horas: \n")
        SeverityEntry = controller.requirement5(cont, hora1, hora2)
        pairs5 = [('Severity', 'key'), ('accidentes', 'value'), ('porcentaje', 'percent')]
        Print1(SeverityEntry['list'], pairs5)
        print('total de accidentes', SeverityEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 6:
        lat = input("latitud: ")
        lng = input('longitud: ')
        distancia = input('distancia: ')
        pairs6 = [('Weekday', 'key'), ('accidentes', 'value')]
        t1 = perf_counter()
        print("\nBuscando accidentes en la zona ingresada: ")
        SeverityEntry = controller.requirement6(cont, lat, lng, distancia)
        Print1(SeverityEntry['list'], pairs6)
        print('total de accidentes :', SeverityEntry['total'])
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    else:
        break
