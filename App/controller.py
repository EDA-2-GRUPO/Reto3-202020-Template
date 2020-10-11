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

import config as cf
from App import model
import datetime
import csv
from DISClib.ADT import orderedmap as om

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""


# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile2016, accidentsfile2019):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = cf.data_dir + accidentsfile2016
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"), delimiter=",")
    for crime in input_file:
        model.addAccident(analyzer, crime)
    # crimesfile2 = cf.data_dir + accidentsfile2019
    # input_file2 = csv.DictReader(open(crimesfile2, encoding="utf-8"),delimiter=",")
    # for crime in input_file2:
    #     model.addAccident(analyzer, crime)
    # return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def requirement1(cont, date):
    Date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.requirement1(cont, Date.date())


def requirement2(cont, date):
    Date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.requirement2(cont, Date.date())


def requirement3(cont, date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    return model.requirement3(cont, date1.date(), date2.date())


def requirement4(cont, date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    return model.requirement4(cont, date1.date(), date2.date())


def requirement5(cont, time1, time2):
    time1 = model.proxyTime(datetime.time.fromisoformat(time1))
    time2 = model.proxyTime(datetime.time.fromisoformat(time2))
    return model.requirement5(cont, time1, time2)


def requirement6(cont, lat, longi, distance):
    lat = float(lat)
    longi = float(longi)
    distance = float(distance)
    return model.requirement6(cont, lat, longi, distance)


