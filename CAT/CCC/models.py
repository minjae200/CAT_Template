from django.db import models
from CCC.Helper.DateHelper import *

# Create your models here.
class Job(models.Model):
    build_start_time = models.DateTimeField('build start time', default=default_start_time, blank=True)
    branch = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100, default="unknown")
    gerrit_status = models.CharField(max_length=100, default="Ready")
    jira_status = models.CharField(max_length=100, default="Screen")

    def __str__(self):
        return '{}_{}_{}_{}_{}'.format(self.id, self.branch, self.build_start_time, self.gerrit_status, self.assignee)

class Module(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    hash_value = models.CharField(max_length=100)
    register = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return '{}_{}_{}_{}_{}'.format(self.name, self.tag, self.hash_value, self.id, self.register)