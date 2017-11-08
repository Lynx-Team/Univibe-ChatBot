server = 'univibe.database.windows.net'
database = 'UnivibeDB'
username = 'univibe'
password = 'Slasten32'
driver = '{ODBC Driver 13 for SQL Server}'
import pyodbc
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)