from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    barcode = models.CharField(max_length=13)
    price = models.FloatField(null=True)
    discounted_price = models.FloatField(null=True, blank=True)
    borrowed = models.BooleanField(default=False)
    coverImage = models.ImageField(upload_to='bookCovers')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


