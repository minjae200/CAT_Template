import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from CCC.Helper.ScheduleHelper import Scheduler
from CCC.Helper.ObserveHelper import GerritSubject, JiraSubject, Viewer

class ThreadPool:

    def __init__(self, job, user, workers=2):
        self.job = job
        self.user = user
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)
    
    def __del__(self):
        print("delete thread")

    def done(self):
        print("DONE")
        self.thread_pool.shutdown(wait=False)

    def run(self):
        print("This is ThreadPool Run function")
        self._run_scheduler()
        # self._run_observer()

    def _run_scheduler(self):
        self.scheduler = Scheduler(self.user)
        self.scheduler.register(self.job)
        # scheduler_futures = [self.thread_pool.submit(self.scheduler.register, self.job)]
        # for result in as_completed(scheduler_futures):
        #     print(result)
        #     self.done()
    
    def _run_observer(self):
        self.observer = Viewer()
        self.gerrit_subject = GerritSubject(self.user)
        self.jira_subject = JiraSubject(self.user)
        self.observer.register_subject('gerrit')
        observer_pool = ThreadPoolExecutor(max_workers=2)
        observer_future = [
            observer_pool.submit(self.gerrit_subject.observe)
        ]
        if 'Ticket' in self.gerrit_subject.status:
            self.observer.register_subject('jira')
            observer_future.append(observer_pool.submit(self.jira_subject.observe))

        for result in as_completed(observer_future):
            print(result)