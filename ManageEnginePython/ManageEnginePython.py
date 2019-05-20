

# need this to connect to SQL Server
import pyodbc
import pandas


conn_str = (
    r'Driver={SQL Server};'
    r'Server=mau-sql01;'
    r'Database=ServiceDesk;'
    r'Trusted_Connection=yes;'
    )

cnxn = pyodbc.connect(conn_str)
#cursor = cnxn.cursor()

#query currently grabs all open jobs for all techs, and we can filter and sort after adding to dataframes
QueryFile = open("Query.txt", encoding='utf-8')
Query = QueryFile.read()

data = pandas.read_sql(Query,cnxn)
#cursor.execute(Query)

#while 1:
#    row = cursor.fetchone()
#    if not row:
#        break
#    print(row.RequestID , '\t' , row.Technician)#calls something from the select statement record

print(data[['RequestID','Technician']])

cnxn.close()

#this will be a background retrieval to print to somewhere else with

#given a set of data (retrieved from this manner) how do I next want to display it in an editable form?
# then how do I want to save that form to be pulled again by this system and updated by a fresh query run?
# do i want the user interface to have a button to repopulate the timesheet - then look up table values? 
# this seems programmable. I would need to store the time entered as a record identified by the task
# then when pulling again get the last saved data for each of the tasks by task #
# this can be a simple txt file stored in the background
# i would want to do cleanup by overwriting the file.
# it would eventually have the last entered value by task # for all tasks ever but that's ok since
# the text file won't be large
# how do i want to make the form? and how do i want people to have to call it?  this is trickier


