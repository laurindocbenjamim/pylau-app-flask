import mysql.connector

# Replace the placeholders with your actual database credentials
host = '185.12.116.142'  #185.12.116.142/herokupylau
user = 'iledmdpt_admin'
password = 'takagEw5FVpy'
database = 'iledmdpt_octech'
port = 3306
#connection = None
# Establish a connection to the database
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port)
    )
    print("Connection established successfully!")
    
    # Perform database operations here
    #print("Database version:", connection.get_server_info())
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from users;")
    resp = cursor.fetchall()
    print(resp)
except mysql.connector.Error as error:
    print("Error while connecting to the database:", error)
except Exception as e:
    print("Another error occurred:", e)

