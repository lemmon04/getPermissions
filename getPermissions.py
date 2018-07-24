import arcpy, pyodbc, os, sys, glob, xlwt
global table_Set
global group_Set
global DomainUsers_rights
global GIS_Team_rights


#########################################################################################
sde_conn ="C:/test.sde"

arcpy.env.workspace = sde_conn
fcList = arcpy.ListFeatureClasses()
table_Set = set([])
DomainUsers_rights = []
GIS_Team_rights = []

def GetPrivileges():
    cnxn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server}'
        r';SERVER='
        r';DATABASE='
        r';Trusted_connection=yes'
        )
    command = "EXEC sp_table_privileges @table_name = " + table_name 
    cursor = cnxn.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    #List of User Group names
    Users_List = [""]
    #List of User Group rights
    Rights_List = []
    i = 0
    for x in Users_List:
        for row in result:
            if row[4] == x:
                if row[5] in ("UPDATE", "INSERT", "DELETE"):
                    table_Set.add(row[2])
                    Rights_List[i].append("editor")
                    break
                elif row[5] == "SELECT":
                    table_Set.add(row[2])
                    Rights_List[i].append("viewer")
            elif row == result[-1]:
                Rights_List[i].append("No data")
            else:
                continue
        i = i + 1

    for row in result:
        if row[4] == "NYDOT\Domain Users":
            if row[5] in ("UPDATE", "INSERT", "DELETE"):
                table_Set.add(row[2])
                DomainUsers_rights.append("editor")
                break
            elif row[5] == "SELECT":
                table_Set.add(row[2])
                DomainUsers_rights.append("viewer")
        else:
            continue
    
        
for fc in fcList:
    split = fc.split(".")
    table_name = split[2]
    GetPrivileges()

    
#Create excel spreadsheet    
book = xlwt.Workbook()
sheet_Permissions = book.add_sheet("Permissions")
style_string = "font: bold on"
bold = xlwt.easyxf(style_string)
#Set column width
sheet_Permissions.col(0).width  = 8000
sheet_Permissions.col(1).width  = 6000
sheet_Permissions.col(2).width  = 6000
sheet_Permissions.col(3).width  = 6000
sheet_Permissions.col(4).width  = 6000
sheet_Permissions.col(5).width  = 6000
sheet_Permissions.col(6).width  = 6000
sheet_Permissions.col(7).width  = 6000
sheet_Permissions.col(8).width  = 6000
sheet_Permissions.col(9).width  = 6000
#Set first row height
sheet_Permissions.row(0).height_mismatch = True
sheet_Permissions.row(0).height = 500
#Set column header names in bold, wrap text
styles = xlwt.XFStyle()
styles.alignment.wrap = 1
font = xlwt.Font()
font.bold = True
styles.font = font
#Set each header with name of AD user groups
sheet_Permissions.write(0,0,'Table', styles)
sheet_Permissions.write(0,1,'NVDOT\', styles)
sheet_Permissions.write(0,2,'NVDOT\', styles)
sheet_Permissions.write(0,3,'NVDOT\, styles)
sheet_Permissions.write(0,4,'NVDOT\', styles)
sheet_Permissions.write(0,5,'NVDOT\', styles)
sheet_Permissions.write(0,6,'NVDOT\', styles)
sheet_Permissions.write(0,7,'NVDOT\', styles)
sheet_Permissions.write(0,8,'NVDOT\', styles)
sheet_Permissions.write(0,9,'NVDOT\', styles)
#Freeze top cell
sheet_Permissions.set_panes_frozen(True)
sheet_Permissions.set_horz_split_pos(1)
sheet_Permissions.set_vert_split_pos(1)
#start from first cell below header
row_Table = 1
col_Table = 0
table_List = list(table_Set)
table_List.sort()
#Add Tables to first column
for x in table_List:
    sheet_Permissions.write(row_Table, col_Table, x)
    row_Table = row_Table + 1
#Add User Rights Data

#list of user rights lists
#draw_List = []
#
col = 1
rows = 1
for rights_list in draw_List:
    for record in rights_list:
        sheet_Permissions.write(rows, col, record)
        rows = rows + 1
    col = col + 1
    rows = 1

#Save book

#############################################################    
book.save("C:\Users\mlemmon\Desktop\Michael\Permissions.xls")

