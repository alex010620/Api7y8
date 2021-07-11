import pyodbc
server = 'tarea7y8.database.windows.net'
database = 'tarea7y8'
username = 'ADM-YAMC'
password = "Ya95509550"  
driver= '{ODBC Driver 17 for SQL Server}'

conexion = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)