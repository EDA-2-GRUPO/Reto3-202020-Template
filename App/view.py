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
from DISClib.DataStructures import listiterator as lstit

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
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("0- Salir")
    print("*******************************************")

def Printlistafinal(lista):
    it=0
    w=lstit.newIterator(lista)
    while lstit.hasNext(w):
        x=lstit.next(w)
        print(x)
        if it==0:
            print("fecha con más accidentes"+str(x))
        elif it==1:
            print("cantidad total de accidentes"+str(x))
        elif it==2:
             print("cantidad de accidentes de la fecha dada" +str(x))
        it+=1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de crimenes ....")
        t1 = perf_counter()
        controller.loadData(cont, crimefile,crimefile2)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
    elif int(inputs[0]) == 4:
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha =input("fecha")
        t1 = perf_counter()
        w = controller.rango_de_fechas(cont,"None",fecha)
        Printlistafinal(w)
        t2 = perf_counter()
        print("tiempo de carga:", t2 - t1)
    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        print("\nBuscando crimenes en un rango de fechas: ")
        fecha =input("fecha")
        t1 = perf_counter()
        w = controller.fecha(cont,fecha)
        print(w)
        t2 = perf_counter()
    else:
        sys.exit(0)
sys.exit(0)
