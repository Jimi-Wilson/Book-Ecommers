from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    barcode = models.CharField(max_length=13)
    price = models.FloatField(null=True)
    cover = models.ImageField(upload_to='/bookCovers')
    description = models.CharField(max_length=400)
    visable = models.BooleanField(default=True)
    stock = models.IntegerField(null=True)