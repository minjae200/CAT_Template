from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from CCC.Helper.GerritHelper import Gerrit
from CCC.Helper.JiraHelper import Jira
import threading, time

class Subject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_observer(self):
        pass

    @abstractmethod
    def remove_observer(self):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

class Observer:
    @abstractmethod
    def update(self, status):
        pass

    @abstractmethod
    def register_subject(self, subject):
        pass

class GerritSubject(Subject):

    def __init__(self, user):
        super().__init__()
        self.gerrit = Gerrit(user)
        self.observer_list = []
        """
        CCC status
        main page 추가사항 : (고민할 것)
        1) JIRA2 URL, Gerrit URL, BUILD IMAGE LINK 각각 표시
        2) RESULT? 에 1) 항목 포함시키기 (Modal) 
        ['Ready', 'In Progress', 'Complete']
        + [ 'Ticket', 'TAS', 'Build']
        """
        self.status = ['Ready']

    def register_observer(self, observer):
        if not observer in self.observer_list:
            self.observer_list.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)
    
    def notify_observers(self):
        for observer in self.observer_list:
            observer.update(page_type='gerrit', status=self.status)

    def get_status(self):
        return []

    def set_status(self, status):
        self.status = status
        self.notify_observers()

    def observe(self):
        while True:
            status = self.get_status()
            if status:
                self.set_status(status)
            if 'Complete' in status:
                break
            time.sleep(60)
        return 'Gerrit Complete'

class JiraSubject(Subject):

    def __init__(self, user):
        super().__init__()
        self.jira = Jira(user)
        self.observer_list = []
        """
        status = ['Screen', 'Confirm', 'Approval', 'Build']
        """
        self.status = ['Screen']

    def register_observer(self, observer):
        if not observer in self.observer_list:
            self.observer_list.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)
    
    def notify_observers(self):
        for observer in self.observer_list:
            observer.update(page_type='jira', status=self.status)

    def get_status(self):
        return []

    def set_status(self, status):
        self.status = status
        self.notify_observers()

    def observe(self):
        while True:
            status = self.get_status()
            if status:
                self.set_status(status)
            if 'Build' in status: # 종료조건 확인할 것 (Build말고 뭐 있엇을듯)
                break
            time.sleep(60)
        return 'Jira Complete'

class Viewer(Observer):

    def __init__(self):
        self.gerrit_status = []
        self.jira_status = []
        self.viwer = {
            'gerrit': [],
            'jira': []
        }

    def update(self, page_type, status):
        if page_type == 'jira':
            pass
        elif page_type == 'gerrit':
            pass
        self.notify()

    def register_subject(self, subject):
        self.viwer[subject].register_observer(self)

    def notify(self):
        print('CCC Status')
        print('gerrit status : {}'.format(self.gerrit_status))
        print('jira status : {}'.format(self.jira_status))
        # 여기서 django로 넘겨줘야함..