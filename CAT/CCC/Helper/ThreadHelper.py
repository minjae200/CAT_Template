import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from CCC.Helper.ObserveHelper import GerritSubject, JiraSubject, Viewer

class ObserverPool:

    def __init__(self, job, gerrit, workers=4):
        self.job = job
        self.gerrit = gerrit
        self.jira = None
        self.observer_pool = ThreadPoolExecutor(max_workers=workers)
        self.observer_future = []
    
    def __del__(self):
        print("delete thread")

    def done(self):
        print("DONE")
        self.observer_pool.shutdown(wait=False)

    def check_status(self):
        print("check_status call")
        delay_time = 10
        while True:
            print('check_status : {}'.format(self.viewer.gerrit_status))
            if self.viewer.gerrit_status == 'MAKE TICKET':
                self.observer.register_subject('jira')
                self.observer_future.append(self.observer_pool.submit(self.jira_subject.observe))
            if self.viewer.gerrit_status == 'TEST PASS':
                delay_time = 300
            # if self.viewer.jira_subject.status == 'APPROVAL':
            #     delay_time = 300
            if self.viewer.gerrit_status == 'COMPLETE':
                break
            time.sleep(delay_time)
        return True
    
    def run_observer(self):
        self.viewer = Viewer(job=self.job, gerrit=self.gerrit)
        self.viewer.register_subject('gerrit')
        self.observer_future = [
            self.observer_pool.submit(self.viewer.gerrit_subject.observe),
            self.observer_pool.submit(self.check_status)
        ]
        for result in as_completed(observer_future):
            print("future :{}".format(result.result()))

