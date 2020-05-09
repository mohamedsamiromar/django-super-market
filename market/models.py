from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price_sale = models.FloatField()
    price_cost = models.FloatField()
    qty = models.IntegerField(default=0)

class Order(models.Model):
    total_qty = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
