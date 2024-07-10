import mysql.connector
from datetime import datetime, timedelta, timezone

# Replace the placeholders with your actual database credentials


def test_mysql_connection():
    host = ''  #
    user = ''
    password = ''
    database = ''
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


# kwargs
def sum_calc(**kwargs):
    num1 = kwargs.get('num1', 0)
    num2 = kwargs.get('num2', 0)
    num3 = kwargs.get('num3', 0)
    return num1 + num2 + num3


# arbitrary arguments *args
def get_object_data(*args, sep=','):
    data = sep.join(args)
    return data

# Anotations
def names(name: str, age: int = 0)-> str and bool: # type: ignore
    """
    Joins a name and age of a person
    """
    print("Annotations:", names.__annotations__)
    print("Arguments:", name, age)
    return f'{name} is {age}', True

date_now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
date_now_tz = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
CALC_DATE = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
CALC_DATE_2 = datetime.now() + timedelta(minutes=30)
print(f'DATE NOW: {datetime.now().strftime('%Y')}')

print(f'SUM: {sum_calc(num1=12, num2=22)}')

print(get_object_data("laurindo", "benjamim", sep=', '))
r1,r2 =names("laurindo", age=12)
print(r1, r2)

