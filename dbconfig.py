import pyodbc

server = 'univibe.database.windows.net'
database = 'UnivibeDB'
username = 'univibe'
password = 'Slasten32'
driver = '{SQL Server}'

cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

PATH_TO_API = 'http://localhost:5000/TelegramAccount/'