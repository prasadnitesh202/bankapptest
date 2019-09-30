from django.db import models

class Toppings(models.Model):
    t_name = models.CharField(max_length=30)