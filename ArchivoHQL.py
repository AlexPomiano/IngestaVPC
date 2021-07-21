
import pandas as pd
import PlantillaExcel as pe

class archivoHQL:

        nombre_hql_perm = "perm.hql"
        nombre_hql_tabla = "table.hql"
        rutaDir=""

        def __init__(self, nom, rutaDir):
                self.nombreExcel = nom
                self.rutaDir=rutaDir

        def genera_hql_tabla(self):

                ob = pe.plantillaExcel(self.nombreExcel)
                datos = ob.LeerExcelTabla()

                QUERY_DDL = "SELECT " + "\n"
                for index, row in datos.iterrows():
                    if index >= 1:
                        QUERY_DDL += ","
                    QUERY_DDL += "CASE WHEN UPPER(TRIM(" + row["CAMPO"] + "))='NULL' THEN NULL ELSE TRIM(" + row[
                        "CAMPO"] + ") END AS " + row["CAMPO"] + "\n"

                QUERY_DDL += "CAST(fecinformacion AS bigint)  AS  fecinformacion" + "\n"
                QUERY_DDL += "FROM ${hiveconf:tableinput}" + "\n"
                QUERY_DDL += "WHERE  fecinformacion='${hiveconf:fecha}'" + "\n"

                NOMBRE_TABLA = self.rutaDir + "\\" + ob.NombreTabla() + ".hql"

                with open(NOMBRE_TABLA, 'w', encoding="utf-8") as archivoHQL:
                    archivoHQL.write(QUERY_DDL)
                    archivoHQL.closed

        def genera_hql_perm(self):

            ob = pe.plantillaExcel(self.nombreExcel)
            datos = ob.LeerExcelTabla()

            query_perm_ddl = "CREATE TABLE ${hiveconf:perm_table} (" + "\n"

            for index, row in datos.iterrows():
                if index >= 1:
                    query_perm_ddl += ","
                query_perm_ddl += row["CAMPO"] + "  String" + "\n"

            query_perm_ddl += ") PARTITIONED BY (fecinformacion string) " + "\n"
            query_perm_ddl += "ROW FORMAT SERDE " + "\n"
            query_perm_ddl += "      'org.apache.hadoop.hive.ql.io.orc.OrcSerde' " + "\n"
            query_perm_ddl += "STORED AS INPUTFORMAT " + "\n"
            query_perm_ddl += "      'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'" + "\n"
            query_perm_ddl += "OUTPUTFORMAT " + "\n"
            query_perm_ddl += "      'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'" + "\n"
            query_perm_ddl += "LOCATION" + "\n"
            query_perm_ddl += "      '${hiveconf:hdfs_perm_path}'" + "\n"

            with open(self.rutaDir + "\\" + self.nombre_hql_perm, 'w', encoding="utf-8") as archivoPermHql:
                archivoPermHql.write(query_perm_ddl)
                archivoPermHql.closed


