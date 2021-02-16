from django.db import models
from CCC.Helper.DateHelper import *

# Create your models here.
class Job(models.Model):
    build_start_time = models.DateTimeField('build start time', default=default_start_time, blank=True)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return '{}_{}'.format(self.branch, self.build_start_time)

class Module(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    hash_value = models.CharField(max_length=100)

    def __str__(self):
        return '{}_{}_{}_{}'.format(self.name, self.tag, self.hash_value, self.id)