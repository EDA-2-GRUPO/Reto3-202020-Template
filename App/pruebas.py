import config as cf
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
sap=m.newMap(numelements=2,
             maptype='PROBING',
             comparefunction=compareOffenses)
m.put(sap,"gonolea",10)
print(sap)
print(m.contains(sap,"gonolea"))
w=m.get(sap,"gonolea")["value"]
print(w)
