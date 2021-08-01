from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from accounts.models import User


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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True)
    trasaction_id = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Book, on_delete=SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total