import arcpy, pyodbc, os

sde_conn ="connection to geodatabase"
arcpy.env.workspace = sde_conn
fcList = arcpy.ListFeatureClasses()


def GetPrivileges():
    cnxn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server}'
        r';SERVER=name of server'
        r';DATABASE=name of db'
        r';Trusted_connection=yes'
        )
    command = "EXEC sp_table_privileges @table_name = " + table_name 
    cursor = cnxn.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    Domain_Users = {"table": set(), "group": set(), "rights": set()}
    GIS_Team = {"table": set(), "group": set(), "rights": set()}
    stuff = []
    for row in result:
        if row[4] == "NVDOT\Domain Users":
            if row[5] == "SELECT":
                Domain_Users["table"].add(row[2])
                Domain_Users["group"].add(row[4])
                Domain_Users["rights"].add("viewer")

            elif row[5] in ("UPDATE", "INSERT", "DELETE"):
                Domain_Users["table"].add(row[2])
                Domain_Users["group"].add(row[4])
                Domain_Users["rights"].add("editor")

        elif row[4] == "NVDOT\GIS Team":
            if row[5] == "SELECT":
                GIS_Team["table"].add(row[2])
                GIS_Team["group"].add(row[4])
                GIS_Team["rights"].add("viewer")

            elif row[5] in ("UPDATE", "INSERT", "DELETE"):
                GIS_Team["table"].add(row[2])
                GIS_Team["group"].add(row[4])
                GIS_Team["rights"].add("editor")

    print list(Domain_Users["table"]) + list(Domain_Users["group"]) + list(Domain_Users["rights"])
    print list(GIS_Team["table"]) + list(GIS_Team["group"]) + list(GIS_Team["rights"])
    print "\n"

for fc in fcList:
    split = fc.split(".")
    table_name = split[2]
    GetPrivileges()

