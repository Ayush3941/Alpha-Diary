from django.db import models


class contactM(models.Model):
	ied=models.CharField(max_length = 15,primary_key =True,auto_created=True)
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=100)
	contactno = models.CharField(max_length = 15)
	enqtxt = models.CharField(max_length = 500)
	regdate = models.DateTimeField()

class Task(models.Model):
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
class Budget(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    number = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.number}"