import mysql.connector
from datetime import datetime, timedelta, timezone

# Replace the placeholders with your actual database credentials


class SimpleClass(object):
    _name = None
    _age = None

    def __init__(self, name: str = None, age:int = None) -> None:
        self._name = name
        self._age = age
    
    def getPeople(self):
        return f'Name {self._name} Age {self._age}'
    


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

data = {"name": "Laura", "age": 12}
def get_name(name = dict):
    print(name['name'])
get_name(name = data)

name = "laurindo"
if name in "laurind":
    print("My name is LAURINDO")


print(SimpleClass().getPeople())

number = 12.3
if not isinstance(float(number), float):
    print("Invalid type value")

long_string=f"""
Hi Laurindo Benjamim,

We're sorry that you were not able to attend Illinois Tech Master of Data Science: Deep Dive on Linear Regression Courses.

If you would like to view the webinar, click here: https://youtu.be/S5ystg9tcGw.

Once you have had the opportunity to learn more about the program and the linear regression math courses you can expect from one of Illinois Tech's top professors, we encourage you to enroll!

As a reminder, the Master of Data Science program at Illinois Tech accepts up to 6 credits from prior learning on Coursera.

To learn more, join enrollment counselor, Aida Rodriguez, on August 14th at our exclusive office hours session. Register here: https://zoom.us/webinar/register/7017217643139/WN_ouroLEq5RD-0qUUZePhvEg.

We look forward to reviewing your enrollment before the August 26th deadline!

Thank you!
Illinois Tech Team
    """
print(f"Size : {len(long_string)}")



required = ['prod_code', 'prod_price', 'prod_img']
key = 'prod_img'

if key in required:
    print(f'The {key.replace('_', ' ').upper()} field is required')




