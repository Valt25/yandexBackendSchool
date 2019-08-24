from django.db import models

# Create your models here.


class Citizen(models.Model):
    citizen_id = models.PositiveIntegerField()
    town = models.TextField()
    street = models.TextField()
    building = models.TextField()
    appartement = models.PositiveIntegerField()
    name = models.TextField()
    birth_date = models.DateField()
    gender = models.BooleanField()
    relatives = models.ManyToManyField('Citizen')

    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='citizens')


class Collection(models.Model):
    pass
