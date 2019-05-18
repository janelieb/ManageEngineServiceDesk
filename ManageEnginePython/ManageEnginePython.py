

# need this to connect to SQL Server
import pyodbc

conn_str = (
    r'Driver={SQL Server};'
    r'Server=mau-sql01;'
    r'Database=ServiceDesk;'
    r'Trusted_Connection=yes;'
    )
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
cursor.execute("Select * from AaaUser where FIRST_NAME like 'Jane%'")

while 1:
    row = cursor.fetchone()
    if not row:
        break
    print(row.FIRST_NAME)#calls something from the select statement record
cnxn.close()


