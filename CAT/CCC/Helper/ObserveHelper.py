from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from CCC.Helper.JiraHelper import Jira
from CCC.Helper.GerritHelper import Gerrit
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from CCC.models import Job, Module
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

    def __init__(self, gerrit):
        super().__init__()
        self.gerrit = gerrit
        self.gerrit_id = gerrit.gerrit_id
        self.observer_list = []
        self.status = 'Ready'
        """
        CCC status
        main page 추가사항 : (고민할 것)
        1) JIRA2 URL, Gerrit URL, BUILD IMAGE LINK 각각 표시
        2) RESULT? 에 1) 항목 포함시키기 (Modal) 
        ['Ready', 'In Progress', 'Complete']
        + [ 'Ticket', 'TAS', 'Build']
        """
        self.status = 'Ready'

    def register_observer(self, observer):
        if not observer in self.observer_list:
            self.observer_list.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)
    
    def notify_observers(self):
        for observer in self.observer_list:
            observer.update(page_type='gerrit', status=self.status)

    def set_status(self, status):
        self.status = status
        self.notify_observers()

    def observe(self):
        print("GerritSubject observe call")
        delay_time = 10
        pre_status = None
        while True:
            status = self.gerrit.get_status()
            if status != pre_status:
                pre_status = status
                self.set_status(status)
            if 'COMPLETE' == status:
                print("GerritSubject ovserve Break")
                break
            if 'BUILDING' == status: delay_time = 300
            elif 'BUILD SUCCESS' == status: delay_time = 10
            elif 'TESTING' == status: delay_time = 300
            elif 'TEST PASS' == status or 'TEST FAIL' == status: delay_time = 10
            print("observe :{}".format(status))
            time.sleep(delay_time)
        return True

class JiraSubject(Subject):

    def __init__(self, user):
        super().__init__()
        self.jira = Jira(user)
        self.observer_list = []
        """
        status = ['Screen', 'Confirm', 'Approval', 'Build']
        """
        self.status = 'Screen'

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
        return None

    def set_status(self, status):
        self.status = status
        self.notify_observers()

    def observe(self):
        print("OBSERVER")
        delay_time = 10
        pre_status = None
        while True:
            status = self.get_status()
            if status != pre_status:
                self.set_status(status)
            if 'COMPLETE' == status:
                break
            if 'BUILDING' == status: delay_time = 300
            elif 'BUILD SUCCESS' == status: delay_time = 10
            elif 'TESTING' == status: delay_time = 300
            elif 'TEST PASS' == status or 'TEST FAIL' == status: delay_time = 10
            print(status)
            time.sleep(delay_time)
        return True

class Viewer(Observer):

    def __init__(self, job, gerrit):
        self.gerrit_status = 'Ready'
        self.jira_status = 'Ready'
        self.job = job
        self.gerrit = gerrit
        self.user = gerrit.user
        self.gerrit_subject = GerritSubject(gerrit)
        # self.jira_subject = JiraSubject(gerrit)

    def update(self, page_type, status):
        if page_type == 'jira':
            print('jira가 업데이트 되었습니다. : {}'.format(status))
            self.jira_status = status
        elif page_type == 'gerrit':
            print('gerrit이 업데이트 되었습니다. : {}'.format(status))
            self.gerrit_status = status
        self.notify()

    def register_subject(self, subject):
        if subject == 'gerrit':
            self.gerrit_subject.register_observer(self)
        elif subject == 'jira':
            self.jira_subject.register_observer(self)

    def notify(self):
        print('gerrit status : {}'.format(self.gerrit_status))
        try:
            job = Job.objects.get(pk=self.job.id)
            job.gerrit_status = self.gerrit_status
            print(job)
            job.save()
            print(job)
            job = get_object_or_404(Job, pk=self.job.id)
            print(job)
        except:
            pass
        return HttpResponseRedirect(reverse('CCC:main'))
        # print('jira status : {}'.format(self.jira_status))

if __name__ == '__main__':
    viewer = Viewer(user={'username': 'sel.autolab', 'password': 'automation2019! '})
    viewer.register_subject('jira')
    viewer.register_subject('gerrit')

    viewer.viewer['gerrit'].set_status('good')
    viewer.viewer['jira'].set_status('bad')
    viewer.viewer['gerrit'].set_status('WOW!')