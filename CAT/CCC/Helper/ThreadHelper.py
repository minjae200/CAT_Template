import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from CCC.Helper.ScheduleHelper import Scheduler
from CCC.Helper.ObserverHelper import Observer

class ThreadPool:

    def __init__(self, workers=3):
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)
        self.futures = []

    def run(self):
        self._run_observer()
        self._run_scheduler()
        self._run_writer()

    def _run_scheduler(self):
        self.scheduler = Scheduler()
        self.futures.append(self.thread_pool.submit(self.scheduler.run()))
    
    def _run_observer(self):
        self.observer = Observer()
        self.futures.append(self.thread_pool.submit(self.observer.run()))
    
    def _run_writer(self):
        self.writer = Writer()
        self.futures.append(self.thread_pool.submit(self.writer.run()))
    