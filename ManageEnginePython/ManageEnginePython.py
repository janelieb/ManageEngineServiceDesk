

# need this to connect to SQL Server
import pyodbc
import pandas

#need to import a code freeze library (pyinstaller)
#need to import a requests library (requests)

#program variables

#connection string. can change server / database
conn_str = (
    r'Driver={SQL Server};'
    r'Server=mau-sql01;'
    r'Database=ServiceDesk;'
    r'Trusted_Connection=yes;'
    )



#query currently grabs all of yesterday's timelogs for all techs if the task has a comment like %wrike%id%

QueryFile = open("QueryWrike.txt", encoding='utf-8')
Query = QueryFile.read()

#hyperlink strings
#format of api command to post to wrike (the time log info) with wrike id from last col of sql

#this will be a background retrieval to print to somewhere else with
cnxn = pyodbc.connect(conn_str)
data = pandas.read_sql(Query,cnxn)

#Creating hyperlink logic

#need to put together hyperlinks from this data
DataToShow = data.filter(items=['Worked_On_Date','TimeMins','TimeSpent_Formatted','Title','FIRST_NAME','WrikeID','ItemID'])



#numeric task id from manage engine
task_numeric = 'numeric wrike id in comment'
time_hrs_str = 'get time in hours as a string from manage engine query'
dateYesterday = 'yyyy-mm-dd'
time_log_comment = 'logged from task id'

#url to get task id from wrike given numeric id
url_get = 'https://www.wrike.com/api/v4/tasks?permalink=https://www.wrike.com/open.htm?id='
task_str = 'getFromURL'




#put together post command url
url_str = 'https://www.wrike.com/api/v4/tasks/'+task_str+'timelogs?hours='+ time_hrs_str + '&trackedDate=' + dateYesterday + '&comment='+ time_log_comment




print(DataToShow)

#close files
QueryFile.close()
cnxn.close()


