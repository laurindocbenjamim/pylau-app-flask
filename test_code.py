import mysql.connector
from datetime import datetime, timedelta, timezone

# Replace the placeholders with your actual database credentials


def test_mysql_connection():
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


date_now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
date_now_tz = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
CALC_DATE = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
CALC_DATE_2 = datetime.now() + timedelta(minutes=30)
print(f'DATE NOW: {CALC_DATE}')

