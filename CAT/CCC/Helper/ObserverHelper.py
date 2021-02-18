from abc import ABCMeta, abstractmethod
from CCC.Helper.RestHelper import Rest

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

class Gerrit(Subject):

    def __init__(self):
        super().__init__()
        self.observer_list = []

    def register_observer(self, observer):
        if not observer in self.observer_list:
            self.observer_list.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)
    
    def notify_observers(self):
        for observer in self.observer_list:
            observer.update()
    
class Viewer(Observer):

    def __init__(self):
        self.gerrit = None
        self.build = False
        self.tas = False
        self.ticket = False

    def update(self, build=False, tas=False, ticket=False):
        self.build = build
        self.tas = tas
        self.ticket = ticket
        self.notify()

    def register_subject(self, gerrit):
        self.gerrit = gerrit
        self.gerrit.register_observer(self)

    def notify(self):
        pass

