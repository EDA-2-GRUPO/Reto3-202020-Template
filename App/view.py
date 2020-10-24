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
from App import controller as cnt
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
    for _ in range(g['size']):
        el = it.next(iterator)
        text = f"[ {el['key']}  ]   "
        for pair in pairs:
            text += pair[0] + " : " + str(el[pair[1]]) + "  "
        print(text)


def PrintMaxEntry(entry, reference):
    i = 0
    for v in entry.values():
        print(f'{reference[i]} : {v}')
        i += 1


"""
Funciones de Printeo
"""


def inicializar():
    print("\nInicializando....")
    C1 = input("inserte 1 para BST y 2 para RBT")
    # cont es el controlador que se usará de acá en adelante
    cont_i = cnt.init(C1)
    return cont_i


def infoPrints():
    print('Cantidad de fechas restrigadas: ', cnt.sizeOmap(dateIndex))
    print('altura del dateIndex: ', cnt.heightOmap(dateIndex))
    print('Cantidad de Horas registradas: ', cnt.sizeOmap(timeIndex))
    print('altura del TimeIndex: ', cnt.heightOmap(timeIndex))
    print('Cantidad de cordenadas registradas: ', cnt.sizeOmap(zoneIndex))
    print('altura del zoneIndex: ', cnt.heightOmap(zoneIndex))


def validacion(cargo, Index, nameIndex):
    if not cargo:
        print('necesita cargar los datos')
        return False
    elif cnt.sizeOmap(Index) == 0:
        print(f'no se ha cargado el {nameIndex}')
        return False
    return True


def main(cont):
    cargo = False
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>') + ' '
        intp = inputs[0]
        if intp == "w":
            del cont
            cont = inicializar()
            cargo = False

        elif intp == "q":
            list_files = []
            print("\nCargando información de accidentes ....")
            print(' En formato 1,2,3,4')
            C2 = input('ingrese los años 2016: 1, 2017: 2, 2018: 3, 2019: 4')
            t1 = perf_counter()
            for nm in C2.split(','):
                list_files.append(dict_files[nm])
            cnt.loadData(cont, list_files)
            t2 = perf_counter()
            print("tiempo de carga:", t2 - t1)
            cargo = True
            infoPrints()
            del list_files, C2, t1, t2

        elif intp == '1':
            if not validacion(cargo, dateIndex, 'dateIndex'):
                continue
            else:
                fecha = input("Ingrese la fecha a consultar\n")
                t1 = perf_counter()
                print('...')
                dateEntry = cnt.getDateInfo(dateIndex, fecha)
                if dateEntry is None:
                    del dateEntry, fecha, t1
                    print('No se encontro la fecha')
                    continue
                print(f'para la fecha {fecha} \n')
                print('|| Accidentes por severidad ||')
                PrintListEntry(dateEntry['list'], [('accidentes', 'value')])
                print('total de accidentes', dateEntry['total'])
                print('')
                t2 = perf_counter()
                print("tiempo de carga:", t2 - t1)
                del dateEntry, fecha, t1, t2

        elif intp == '2':
            if not validacion(cargo, dateIndex, 'dateIndex'):
                continue
            else:
                fecha = input("Ingrese la fecha posterior a la busqueda: \n")
                t1 = perf_counter()
                print('...')
                maxSeverity = cnt.mstFreqDateBfADate(dateIndex, fecha)
                print(f'para antes de la fecha: {fecha} \n')
                print('|| fecha con mas accidentes ||')
                PrintMaxEntry(maxSeverity, ['fecha', 'numero de accidentes', 'total accidentes'])
                print('')
                t2 = perf_counter()
                print("tiempo de carga:", t2 - t1)
                del fecha, maxSeverity, t1, t2

        elif intp == '3':
            if not validacion(cargo, dateIndex, 'dateIndex'):
                continue
            else:
                fecha1 = input('fecha 1\n')
                fecha2 = input('fecha 2\n')
                t1 = perf_counter()
                print('...')
                maxSeverity = cnt.mstFreqSeverityInRgDates(dateIndex, fecha1, fecha2)
                print(f'para el rango de fechas: {fecha1} a {fecha2} \n')
                print('|| Severidad mas frecuente ||')
                PrintMaxEntry(maxSeverity, ['Severidad', 'numero de accidentes', 'total accidentes'])
                t2 = perf_counter()
                print('')
                print("tiempo de carga:", t2 - t1)
                del fecha1, fecha2, maxSeverity, t1, t2

        elif intp == '4':
            if not validacion(cargo, dateIndex, 'dateIndex'):
                continue
            else:
                fecha1 = input("fecha1")
                fecha2 = input('fecha2')
                t1 = perf_counter()
                print('...')
                maxStateAndDate = cnt.MstFreqDateAndMstFreqStateInRgDates(dateIndex, fecha1, fecha2)
                print(f'para el rango de fechas: {fecha1} a {fecha2} \n')
                print('|| Estado con mas accidentes ||')
                PrintMaxEntry(maxStateAndDate['mstState'], ['Estado', 'accidentes'])
                print('|| Fecha con mas accidentes ||')
                PrintMaxEntry(maxStateAndDate['mstDate'], ['Fecha', 'accidentes'])
                print('')
                t2 = perf_counter()
                print("tiempo de carga:", t2 - t1)
                del fecha1, fecha2, maxStateAndDate, t1, t2

        elif intp == '5':
            if not validacion(cargo, timeIndex, 'timeIndex'):
                continue
            else:
                hora1 = input("time1: ")
                hora2 = input('time2: ')
                t1 = perf_counter()
                print('...')
                r4 = cnt.severityFrequencyListInRgHours(timeIndex, hora1, hora2)
                SeverityEntry = r4['result']
                Haj = r4['horas']
                print(f'para el rango de horas:  {hora1} a {hora2}')
                print(f'ajustadas como {Haj[0]}  a {Haj[1]}\n')
                print('|| Accidentes por severidad ||')
                PrintListEntry(SeverityEntry['list'], [('accidentes', 'value'), ('porcentaje', 'percent')])
                print('total de accidentes', SeverityEntry['total'])
                t2 = perf_counter()
                print('')
                print("tiempo de carga:", t2 - t1)
                del hora1, hora2, SeverityEntry, t1, t2

        elif intp == '6':
            if not validacion(cargo, zoneIndex, 'zoneIndex'):
                continue
            else:
                lat = input("latitud: ")
                lng = input('longitud: ')
                distancia = input('distancia: ')
                # t1 = perf_counter()
                print("\nBuscando accidentes en la zona ingresada: \n"
                      f"latitud: {lat}, longitud: {lng}, a una distancia de {distancia}  \n")
                weekdayEntry = cnt.weekdayFrequencyListInArea(zoneIndex, lat, lng, distancia)
                print('|| Accidentes por dia de la semana||')
                PrintListEntry(weekdayEntry['list'], [('accidentes', 'value')])
                print('total de accidentes :', weekdayEntry['total'])
                t2 = perf_counter()
                print('')
                print("tiempo de carga:", t2 - t1)
                del lat, lng, distancia, weekdayEntry, t1, t2

        elif intp == '0':
            break

        else:
            print('opcion no valida')
            continue
        input('presione cualquier tecla para continuar')


if __name__ == '__main__':
    f_cont = inicializar()
    dateIndex = f_cont.get('dateIndex')
    timeIndex = f_cont.get('timeIndex')
    zoneIndex = f_cont.get("ZoneIndexLatLng")
    main(f_cont)
