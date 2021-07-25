from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    barcode = models.CharField(max_length=13)
    price = models.FloatField(null=True)
    borrowed = models.BooleanField(default=False)
    coverImage = models.ImageField(upload_to='bookCovers')

    def __str__(self):
        return self.title
