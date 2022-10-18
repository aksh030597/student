from email.policy import default
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=200)
    div = models.CharField(max_length=5)


    def __str__(self):

        return self.name+" "+self.div

class Payments(models.Model):
    user = models.CharField(max_length=200, unique=True)
    amount = models.IntegerField(default=100)

