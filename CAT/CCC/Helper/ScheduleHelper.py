from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from CCC.Helper.GerritHelper import Gerrit
import time

class Scheduler:
    
    def __init__(self, user):
        self.user = user
        self.worker = BackgroundScheduler()
        self.worker.start()

    def __del__(self):
        print("Scheduler 가 삭제되었습니다.")

    def register(self, job):
        self.job = job
        self.add_job(job=job, func=self.run_job)

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
        if func is None: func = self.run_job
        self.worker.add_job(func, 'cron',
                            year=job.build_start_time.year, month=job.build_start_time.month,
                            day=job.build_start_time.day, hour=job.build_start_time.hour,
                            minute=job.build_start_time.minute, second=0,
                            id=str(job.id), args=[job])
        
    def remove_job(self, job_id):
        try:
            self.worker.remove_job(str(job_id))
        except JobLookupError as error:
            print("Alreay finish or Not exist the scheduler : {}".format(error))
            return
    
    def run_job(self, job):
        gerrit = Gerrit(self.user)
        gerrit.start_CCC(job)
        # self.remove_job(job_id)
        return True
