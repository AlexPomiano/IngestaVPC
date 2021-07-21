# Clase para el manejo de archivos excel
import pandas as pd
import os

class plantillaExcel:


    def __init__(self, nom):
        self.nombre = nom

    def LeerExcelDatos (self):
        datos = pd.read_excel(self.nombre, skiprows=0, sheet_name=0)
        return datos

    def LeerExcelTabla(self):
        datos = pd.read_excel(self.nombre, skiprows=0, sheet_name=1)
        return (datos)

    def LeerExcelIngesta (self):
        datos = pd.read_excel(self.nombre, skiprows=0, sheet_name=2)
        return (datos)

    def NombreTabla (self):
        df = pd.read_excel(self.nombre, skiprows=0, sheet_name=0)
        SQUAD = df.loc[0]["VALOR"]
        INTERFACE = df.loc[3]["VALOR"]
        INICIATIVA = df.loc[4]["VALOR"]
        return (INTERFACE + "_" + SQUAD + "_" + INICIATIVA)

    def getListaPlantillas (self):
        listaPlantillas = os.listdir(self.nombre)
        return listaPlantillas



