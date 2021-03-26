from datetime import datetime, timedelta

def default_start_time():
    now = datetime.now()
    start = now.replace(hour=10, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)

def current_time():
    now = datetime.now()
    return now

def get_time(date, time):
    if date:
        date = list(map(int, date.split('-')))
        year, month, day = date[0], date[1], date[2]
    if time:
        time = list(map(int, time.split(':')))
        hour, minute = time[0], time[1]

    now = datetime.now()
    try:
        start = now.replace(year=year, month=month, day=day)
    except:
        default_time = default_start_time()
        start = now.replace(year=default_time.year, month=default_time.month, day=default_time.day)
    
    try:
       start = start.replace(hour=hour, minute=minute)
    except:
        default_time = default_start_time()
        start = start.replace(hour=default_time.hour, minute=default_time.minute) 
    return start