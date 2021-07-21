import ArchivoJson as aj
import ArchivoHQL as hql
import ArchivoSQL as sql
import os
import PlantillaExcel as excel
import stat as s
from shutil import rmtree
import pandas as listafuentes
import logging
import sys

if __name__ == '__main__':

    logger = logging.getLogger('VPC_Log')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('VPCLog.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    try:
        pathProyecto = os.getcwd()
        logger.info(">>>>> Inicio - Ruta de trabajo : " + pathProyecto)
        pathPlantillasExcel = pathProyecto + "\\" + "PlantillasFuentes"
        logger.info(">>>>> Inicio - Ruta de Plantillas Excel : " + pathPlantillasExcel)
        e = excel.plantillaExcel(pathPlantillasExcel)
        listafuentes=e.getListaPlantillas()
        logger.info(">>>>>>> Lista de planitllas : " + str(listafuentes))
    except OSError as err:
        logger.error("OS error: {0}".format(err))


    for plantilla in listafuentes:
            #leer el nombre de la tabla (será la carpeta) del archivo plantilla
        nomExcel = pathPlantillasExcel + "\\" + plantilla
        e = excel.plantillaExcel(nomExcel)
        pathDir = pathProyecto + "\\" + e.NombreTabla()
        logger.info("***** Inicio - Creación objetos de la fuente: *****")
        try:
            if os.path.exists(pathDir): rmtree(pathDir)
            logger.info("===== Creación de carpeta: " + pathDir)
            os.makedirs(pathDir,mode=s.S_IRWXU)
            a = aj.archivoJson(nomExcel, pathDir)
            logger.info("*** Inicio - creación de archivo de ingesta:" + pathDir)
            a.generaJsonIngesta()
            logger.info("*** Fin - creación de archivo de ingesta:" + pathDir)
            logger.info("*** Inicio - creación de archivo hql:" + pathDir)
            b = hql.archivoHQL(nomExcel, pathDir)
            b.genera_hql_perm()
            b.genera_hql_tabla()
            logger.info("*** Fin - creación de archivo hql:" + pathDir)
            logger.info("*** Inicio - creación de archivo sql:" + pathDir)
            c = sql.archivoSQL(nomExcel, pathDir)
            c.genera_tabla_sql()
            logger.info("*** Fin - creación de archivo sql:" + pathDir)
            logger.info("***** Fin - Creación objetos de la fuente:" + pathDir)
        except OSError as err:
            logger.error("OS error: {0}".format(err))

    logger.info("Fin - Creación de objetos para la ingesta:")

















