from django.db import models


class Store(models.Model):
    city = models.CharField()
    address = models.CharField()


class Sale(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    sale = models.IntegerField()


class OrderStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class Order(models.Model):
    store = models.CharField()
    product = models.CharField()
    status = models.CharField(choices=OrderStatus.choices)


class Employee(models.Model):
    name = models.CharField(primary_key=True)
    manager = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
