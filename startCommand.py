from dbconfig import cnxn
def startMessage():
    cursor = cnxn.cursor()
    cursor.execute("SELECT username FROM AspNetUsers")

    row = cursor.fetchone()
    while row:
        print(str(row))
        row = cursor.fetchone()
    return "what"