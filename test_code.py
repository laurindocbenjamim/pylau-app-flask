import mysql.connector

# Replace the placeholders with your actual database credentials
host = 'herokupylau' #185.12.116.142
user = 'iledmdpt_admin'
password = '#h*zvXb+S6?;'
database = '#h*zvXb+S6?;'
#connection = None
# Establish a connection to the database
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connection established successfully!")
    
    # Perform database operations here
    
except mysql.connector.Error as error:
    print("Error while connecting to the database:", error)
except Exception as e:
    print("Another error occurred:", e)

