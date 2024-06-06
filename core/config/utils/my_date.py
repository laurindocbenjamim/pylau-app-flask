
from datetime import datetime, date, timedelta

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def convert_date_to_int(date_str):
    date_int = int(date_str.timestamp())
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return int(date_obj.timestamp())

# get time remaining returns a dictionary of the time remaining in days, hours, minutes, seconds
def get_time_remaining_JSON(start_date,expiration_date, expire_time, compare_date=datetime.now()):
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#user['created_date']
    created_date = datetime.strftime(start_date,'%Y-%m-%d %H:%M:%S')            
    date_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    date_created_int = int(date_obj.timestamp())
            
    date_now_int = int(datetime.now().timestamp())
   
            
    #date_obj = datetime.strptime(str(created_date), '%a, %d %b %Y %H:%M:%S %Z')
            

    expiration_date = date_obj + timedelta(days=expire_time)

    time_remaining = expiration_date - compare_date
    #time_remaining_int = int(datetime.strptime(str(time_remaining), '%Y-%m-%d %H:%M:%S').timestamp())
    total_seconds = int(time_remaining.total_seconds())
    total_minutes = total_seconds // 60
    total_hours = total_minutes // 60
    time_left_days = total_hours // 24
            
            
    return { 'data': {
        'created_date': date_created_int, 'today': date_now_int,
        'exp_date': str(expiration_date), 'time_REMAINING': str(time_remaining),
        'days_left': time_left_days,'total_hours': total_hours, 'total_minutes': total_minutes, 
        'total_seconds': total_seconds
    }}

