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
from DISClib.ADT import list as lt
from App import controller

assert config
from time import perf_counter
from DISClib.DataStructures import listiterator as it

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
crimefile2 = "us_accidents_dis_2019.csv"


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("w- Inicializar Analizador")
    print("q- Cargar información de accidentes")
    print("1- Requerimento 1")
    print("2- Requerimento 2")
    print("3- Requerimento 3")
    print("4- Requerimento 4")
    print("0- Salir")
    print("*******************************************")


def Print1(g):
    iter = it.newIterator(g)
    for _ in range(lt.size(g)):
        el = it.next(iter)
        sev = el["key"]
        cant = el["value"]
        print("Severity :", sev, "  accidentes :", cant)


"""
Menu principal
"""
while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "w":
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif inputs[0] == "q":
        print("\nCargando información de crimenes ....")
        t1 = perf_counter()
        controller.loadData(cont, crimefile, crimefile2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 1:
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha = input("fecha")
        t1 = perf_counter()
        dateEntry = controller.getDate(cont, fecha)
        SeverityList = controller.Severity_list(dateEntry)
        Print1(SeverityList)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)


    elif int(inputs[0]) == 2:
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha = input("fecha")
        t1 = perf_counter()
        w = controller.requirement2(cont, fecha)
        print(w)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 3:
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha1 = input("fecha1")
        fecha2 = input('fecha2')
        t1 = perf_counter()
        w = controller.requirement3(cont,fecha1,fecha2)
        print(w)
        # Printlistafinal(w)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
    elif int(inputs[0]) == 4:
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha1 = input("fecha1")
        fecha2 = input('fecha2')
        t1 = perf_counter()
        w = controller.requirement4(cont,fecha1,fecha2)
        print(w)
        # Printlistafinal(w)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
    else:
        break

t1 = perf_counter()
for _ in range(320000):
    try:
        pass
    except KeyError:
        pass
t2 = perf_counter()
print(t2 - t1)
