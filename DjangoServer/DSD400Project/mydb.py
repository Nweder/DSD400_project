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
cursorObject.execute("CREATE DATABASE IF NOT EXISTS dsd400")

# Välj databasen
cursorObject.execute("USE dsd400")

# Skriv ut ett meddelande om att allt gick bra
print("Database 'dsd400' is created and selected!")

# Stäng anslutningen
cursorObject.close()
dataBase.close()
