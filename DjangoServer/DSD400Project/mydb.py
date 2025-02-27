import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '123',
    database="mydatabase"  

)

cursorObject = dataBase.cursor()

#creat database
cursorObject.execute("SELECT DATABASE();")
cursorObject.close()
dataBase.close()

print("All DONE!!!!")