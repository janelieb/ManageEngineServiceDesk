

# need this to connect to SQL Server
import pyodbc
import pandas

#from kivy.app import App
#from kivy.uix.label import Label
#need to import a gui library (kivas?)
#need to import a code freeze library (pyinstaller)

#program variables
#Technician variable
Tech = "Jane Lieberman"
#connection string. can change server / database
conn_str = (
    r'Driver={SQL Server};'
    r'Server=mau-sql01;'
    r'Database=ServiceDesk;'
    r'Trusted_Connection=yes;'
    )
#query currently grabs all open jobs for all techs, and we can filter and sort after adding to dataframes
QueryFile = open("Query.txt", encoding='utf-8')
Query = QueryFile.read()
#hyperlink strings
#workorder = Link 1 + ID + Link 2
#project = Link 1 + ID
#Task = Link 1 + ID + Link 2
Workorder_Link_1 = "http://192.168.0.59:8080/WorkOrder.do?woMode=viewWO&woID="
Workorder_Link_2 = "&&fromListView=true"
Project_Link_1 = "http://192.168.0.59:8080/ProjectAction.do?submitaction=ViewProject&fromListView=true&projectid="
Task_Link_1 = "http://192.168.0.59:8080/TaskDefAction.do?submitaction=viewTask&TASKID="
Task_Link_2 = "&from=project&fromListView=true"
Problem_Link_1 = "http://192.168.0.59:8080/ProblemDetails.cc?PROBLEMID="
Problem_Link_2 = "&fromListView=true"

#this will be a background retrieval to print to somewhere else with
cnxn = pyodbc.connect(conn_str)
data = pandas.read_sql(Query,cnxn)
#filter technician as this isn't done in the query to keep the variable passing at closer-to-the top layer
DataByTech = data[data.Technician==Tech]
#Creating hyperlink logic
DataByTech['Link_1']=Workorder_Link_1
DataByTech['Link_2']=Workorder_Link_2
DataByTech['ParentLink_1']=""
DataByTech['ParentLink_2']=""
DataByTech.loc[DataByTech.ParentType=='WorkOrder','ParentLink_1']=Workorder_Link_1
DataByTech.loc[DataByTech.ParentType=='WorkOrder','ParentLink_2']=Workorder_Link_2
DataByTech.loc[DataByTech.RequestType=='Task','Link_1']=Task_Link_1
DataByTech.loc[DataByTech.RequestType=='Task','Link_2']=Task_Link_2
DataByTech.loc[DataByTech.RequestType=='Problem','Link_1']=Problem_Link_1
DataByTech.loc[DataByTech.RequestType=='Problem','Link_2']=Problem_Link_2
DataByTech.loc[DataByTech.ParentType=='Project','ParentLink_1']=Project_Link_1
DataByTech.loc[DataByTech.ParentType=='Project','ParentLink_2']=""
DataByTech.loc[DataByTech.RequestType=='Project','Link_1']=Project_Link_1
DataByTech.loc[DataByTech.RequestType=='Project','Link_2']=""
DataByTech['Link'] = DataByTech['Link_1']+DataByTech['RequestID'].map(str)+DataByTech['Link_2']
DataByTech['ParentLink'] = DataByTech['ParentLink_1']+DataByTech['ParentID'].map(str)+DataByTech['ParentLink_2']
#need to put together hyperlinks from this data
DataToShow = DataByTech.filter(items=['RequestType','RequestID','ParentType','ParentID','Technician','Link','ParentLink','Subject','STATUSNAME','Urgency','Priority'])
print(DataToShow)
#close files
QueryFile.close()
cnxn.close()


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


