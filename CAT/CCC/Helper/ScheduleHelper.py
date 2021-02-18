from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time

class Scheduler:
    
    def __init__(self):
        self.worker = BackgroundScheduler()
        self.worker.start()

    def __del__(self):
        print("Scheduler 가 삭제되었습니다.")
        self.worker.shutdown()

    def add_job(self, job, func):
        """
        year (int|str) – 4-digit year
        month (int|str) – month (1-12)
        day (int|str) – day of the (1-31)
        week (int|str) – ISO week (1-53)
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        hour (int|str) – hour (0-23)
        minute (int|str) – minute (0-59)
        second (int|str) – second (0-59)
        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
        """
        self.worker.add_job(func, 'cron',
                            year=job.build_time.year, month=job.build_time.month,
                            day=job.build_time.day, hour=job.build_time.hour,
                            minute=job.build_time.minute, second=0,
                            id=job.id, args=('cron', job.id))
        
    def remove_job(self, job):
        try:
            self.worker.remove_job(job.id)
        except JobLookupError as error:
            print("Does not exist the scheduler : {}".format(error))
            return


if __name__ == '__main__':
    print("start")
    scheduler = Scheduler()
    scheduler.add_job("1", lambda : print("!!"))
    count = 0
    while count < 300:
        time.sleep(1)
        count += 1
    scheduler.remove_job("1")
    # count = 0
    # while True:
    #     '''
    #     count 제한할 경우 아래와 같이 사용
    #     '''
    #     print("Running main process")
    #     time.sleep(1)
    #     count += 1
    #     if count == 10:
    #         scheduler.kill_scheduler("1")
    #         print("Kill cron Scheduler")
    #     elif count == 15:
    #         scheduler.kill_scheduler("2")
    #         print("Kill interval Scheduler")