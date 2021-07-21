import pandas as pd
import PlantillaExcel as pe


class archivoSQL:

    nombre_tabla_sql = "tabla.sql"
    rutaDir=""

    def __init__(self, nom, rutaDir):
        self.nombreExcel = nom
        self.rutaDir = rutaDir

    def genera_tabla_sql(self):
        # Formateo de Cabecera
        cabecera = "------------------------------------------------------------------------------------------------------" + "\n"
        cabecera += "-- Squad                   : {SQUAD}" + "\n"
        cabecera += "-- Descripción             : {DESCRIPCION}" + "\n"
        cabecera += "-- Fecha de Creación       : {FECHA}" + "\n"
        cabecera += "-- Iniciativa              : {INICIATIVA}" + "\n"
        cabecera += "-- Responsable IBK         : {RESPONSABLE}" + "\n"
        cabecera += "-- Autor                   : {AUTOR}" + "\n"
        cabecera += "-- Proceso completado " + "\n"
        cabecera += "-----------------------------------------------------------------------------------------------------" + "\n"
        cabecera += "-- Nro. (SRT/SRI)          Fecha           Desarrollador     Líder Técnico             Descripción" + "\n"
        cabecera += "-- {SRI}                {FECHA}     {AUTOR}    {LT}            {DESCRIPCION}" + "\n"
        cabecera += "-----------------------------------------------------------------------------------------------------" + "\n"

        ob = pe.plantillaExcel(self.nombreExcel)
        df = ob.LeerExcelDatos()

        SQUAD = df.loc[0]["VALOR"]
        DESCRIPCION = df.loc[1]["VALOR"]
        FECHA = df.loc[2]["VALOR"]
        INTERFACE = df.loc[3]["VALOR"]
        INICIATIVA = df.loc[4]["VALOR"]
        RESPONSABLE = df.loc[5]["VALOR"]
        AUTOR = df.loc[6]["VALOR"]
        LT = df.loc[7]["VALOR"]
        SRI = df.loc[8]["VALOR"]
        AMBIENTE = df.loc[9]["VALOR"]
        PI = df.loc[10]["VALOR"]

        cabecera=cabecera.format(SQUAD=SQUAD, DESCRIPCION=DESCRIPCION, FECHA=FECHA, INICIATIVA=INICIATIVA,
                                  RESPONSABLE=RESPONSABLE,AUTOR=AUTOR,LT=LT,SRI=SRI)

        tabla = "{AMBIENTE}_DW_LANDING.{INTERFACE}_{SQUAD}_{INICIATIVA}"
        tabla = tabla.format(AMBIENTE=AMBIENTE, INTERFACE=INTERFACE, SQUAD=SQUAD, INICIATIVA=INICIATIVA)

        cuerpo = "CREATE MULTISET TABLE {tabla}," + "\n"
        cuerpo += "NO BEFORE JOURNAL," + "\n" + "NO AFTER JOURNAL," + "\n" + "CHECKSUM = DEFAULT," + "\n" + "DEFAULT MERGEBLOCKRATIO," + "\n"
        cuerpo += "MAP = TD_MAP1" + "\n" + "("

        cuerpo = cuerpo.format(tabla=tabla)

        ob = pe.plantillaExcel(self.nombreExcel)
        df1 = ob.LeerExcelTabla()

        # Formateo de Campos
        campos= "\n"
        for index, row in df1.iterrows():
            if index>=1:
                campos += ','
            campos += row["CAMPO"] + " " + row["TIPO DATO"]
            if row["TIPO DATO"] == "VARCHAR":
                campos += " (" + str(int(row["LONGITUD"])) + ")  CHARACTER SET LATIN NOT CASESPECIFIC" + "\n"
            else:
                campos += "\n"

        campos += ", FecInformacion INTEGER)" + "\n"

        if PI=='':
            campos += ";"
        else:
            campos += "PRIMARY INDEX (" + PI + ") ; " + "\n"


        # Formateo de Comentario
        comentario = "\n"
        for index, row in df1.iterrows():
            comentario += ".IF ERRORCODE <> 0 THEN .GOTO ERRORFOUND;" + "\n"
            comentario += "COMMENT ON COLUMN " + tabla + "." + row["CAMPO"] + " IS  '" + row["DESCRIPCIÓN"] + "';" + "\n"

        comentario += ".IF ERRORCODE <> 0 THEN .GOTO ERRORFOUND;" + "\n"
        comentario += "COMMENT ON COLUMN " + tabla + "." + "FecInformacion IS '" + "Fecha de Información'; " + "\n"

        nombre_SQL = self.rutaDir+ "\\" + INTERFACE +"_" + SQUAD + "_" + INICIATIVA + ".sql"

        with open(nombre_SQL,'w',encoding="ANSI",) as archivoSQL:
            archivoSQL.write(cabecera+cuerpo+campos+comentario)
            archivoSQL.closed