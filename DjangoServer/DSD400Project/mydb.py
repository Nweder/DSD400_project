# import mysql.connector

# dataBase = mysql.connector.connect(
#     host = 'localhost',
#     port = '3306',
#     user = 'root',
#     passwd = '12345',
#     # database="MySQL999"  

# )

# cursorObject = dataBase.cursor()

# #creat database
# cursorObject.execute("CREATE DATABASE dsd4001")
# # cursorObject.execute("SELECT DATABASE(dsd400);")
# # cursorObject.close()
# # dataBase.close()

# print("All DONE!!!!")

import mysql.connector

# Anslut till MySQL
dataBase = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    passwd='12345'
)

cursorObject = dataBase.cursor()

# Skapa en databas (om den inte finns redan)
cursorObject.execute("CREATE DATABASE IF NOT EXISTS dsd4001")

# Välj databasen
cursorObject.execute("USE dsd4001")

# Skriv ut ett meddelande om att allt gick bra
print("Database 'dsd4001' is created and selected!")

# Stäng anslutningen
cursorObject.close()
dataBase.close()
