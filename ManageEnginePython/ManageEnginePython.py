

# need this to connect to SQL Server
import pyodbc
import pandas
import PyInstaller
import requests

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


token = 'eyJ0dCI6InAiLCJhbGciOiJIUzI1NiIsInR2IjoiMSJ9.eyJkIjoie1wiYVwiOjE3Mjk2NDYsXCJpXCI6NjM2NzczOSxcImNcIjo0NjEyMzkzLFwidVwiOjU2NzYyMDcsXCJyXCI6XCJVU1wiLFwic1wiOltcIldcIixcIkZcIixcIklcIixcIlVcIixcIktcIixcIkNcIixcIkFcIixcIkxcIl0sXCJ6XCI6W10sXCJ0XCI6MH0iLCJpYXQiOjE1NjI5NTc1Njd9.yHAc30viuUEDyPZ1zabc408hk7MOMaVWFaufbzJHWkI'
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
#need to update this to cycle through each wrike id.
task_numeric = DataToShow['WrikeID'][0]

time_hrs_str = 'get time in hours as a string from manage engine query'
dateYesterday = 'yyyy-mm-dd'
time_log_comment = 'logged from task id'

#url to get task id from wrike given numeric id
url_get = 'https://www.wrike.com/api/v4/tasks?'
permalink = '=https://www.wrike.com/open.htm?id='+task_numeric
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'permalink':permalink} 
# sending get request and saving the response as response object 
r = requests.get(url = url_get, headers = {'Authorization':'Bearer ' +token}, params = PARAMS) 
# extracting data in json format 
dataget = r.json() 
#parse json response
task_str = str(dataget['data'][0]['id'])

print(task_str)

#put together time in hours, date yesterday and time log comment
time_hrs_str = round(float(DataToShow['TimeMins'][0]/60),2)

time_hrs_str = str(time_hrs_str)
print(time_hrs_str)
dateYesterday = str(DataToShow['Worked_On_Date'][0])
print(dateYesterday)
time_log_comment = 'Task' + str(DataToShow['ItemID'][0])
print(time_log_comment)
  
## printing the output 
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      %(latitude, longitude,formatted_address)) 


#put together post command url
url_str = 'https://www.wrike.com/api/v4/tasks/'+task_str+'/timelogs?hours='+ time_hrs_str + '&trackedDate=' + dateYesterday + '&comment='+ time_log_comment

r = requests.post(url = url_str, headers = {'Authorization':'Bearer '+token}) 

print (r.text)

print(DataToShow)
print(url_str)
#close files
QueryFile.close()
cnxn.close()


