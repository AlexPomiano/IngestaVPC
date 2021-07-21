
import pandas as pd
import PlantillaExcel as pe

class archivoJson:

        nombre_json = 'config.json'

        def __init__(self, nomExcel, rutaDir):
                self.nombreExcel = nomExcel
                self.nombre_json = rutaDir + "\\" + self.nombre_json

        def generaJsonIngesta(self):

                ob = pe.plantillaExcel(self.nombreExcel)
                df = ob.LeerExcelIngesta()

                ID_BATCH_LZH = df.loc[0]["VALOR"]
                NOMBRE_FUENTE = df.loc[1]["VALOR"]
                TIPO_FUENTE = df.loc[2]["VALOR"]
                DELIMITAR = df.loc[3]["VALOR"]
                NUM_CAMPOS = df.loc[4]["VALOR"]
                NOM_PROYECTO = df.loc[5]["VALOR"]
                TIPO_CARGA = df.loc[6]["VALOR"]
                CONTROL_M = df.loc[7]["VALOR"]
                FUENTE_USUARIO = df.loc[8]["VALOR"]
                CABECERA = df.loc[9]["VALOR"]

                NOMBRE_TABLA = ob.NombreTabla()

                QUERY_JSON = "{" + "\n"
                QUERY_JSON += ' "definition": { ' + "\n"
                QUERY_JSON += '     "id_batch_lzh":  "' + ID_BATCH_LZH + '",' + "\n"
                QUERY_JSON += '     "source_name":  "' + NOMBRE_FUENTE + '",' + "\n"
                QUERY_JSON += '     "type_source":  "' + TIPO_FUENTE + '",' + "\n"
                QUERY_JSON += '     "column_delimiter":  "' + DELIMITAR + '",' + "\n"
                QUERY_JSON += '     "column_count":  "' + str(NUM_CAMPOS) + '",' + "\n"
                QUERY_JSON += '     "flg_rejected": "",' + "\n"
                QUERY_JSON += '     "redefine_arch": "N",' + "\n"
                QUERY_JSON += '     "redefine_process": "",' + "\n"
                QUERY_JSON += '     "control_file": "N",' + "\n"
                QUERY_JSON += '     "schema_hive": "${PRM_AMB}_perm",' + "\n"
                QUERY_JSON += '     "name_table_hive":  "' + NOMBRE_TABLA + '",' + "\n"
                QUERY_JSON += '     "flg_delivery": "Y",' + "\n"
                QUERY_JSON += '     "transformation_table":   "' + NOMBRE_TABLA + '.hql",' + "\n"
                QUERY_JSON += '     "export_name": "EXPORT_TERADATA",' + "\n"
                QUERY_JSON += '     "target_schema": "${PRM_AMB}_DW_LANDING" ,' + "\n"
                QUERY_JSON += '     "target_table":   "' + NOMBRE_TABLA + '",' + "\n"
                QUERY_JSON += '     "save_lote": "N",' + "\n"
                QUERY_JSON += '     "type_load":  "' + TIPO_CARGA + '",' + "\n"
                QUERY_JSON += '     "project_name":  "' + NOM_PROYECTO + '",' + "\n"
                QUERY_JSON += '     "load": "' + CONTROL_M + '",' + "\n"
                QUERY_JSON += '     "path_user": "' + FUENTE_USUARIO + '",' + "\n"
                QUERY_JSON += '     "group_id": "0",' + "\n"
                QUERY_JSON += '     "concat": "' + CABECERA + '"' + "\n"
                QUERY_JSON += "     }" + "\n"
                QUERY_JSON += "}" + "\n"

                with open(self.nombre_json, 'w', encoding="utf-8") as archivoJson:
                        archivoJson.write(QUERY_JSON)
                        archivoJson.closed





