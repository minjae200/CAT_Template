from datetime import datetime, timedelta

def default_start_time():
    now = datetime.now()
    start = now.replace(hour=10, minute=30, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)

def get_time(date, time):
    if date == None or time == None:
        return None
    if date == '' or time == '':
        return None
    date = list(map(int, date.split('-')))
    year, month, day = date[0], date[1], date[2]
    time = list(map(int, time.split(':')))
    hour, minute = time[0], time[1]
    now = datetime.now()
    start = now.replace(year=year, month=month, day=day, hour=hour, minute=minute, second=0, microsecond=0)
    return start