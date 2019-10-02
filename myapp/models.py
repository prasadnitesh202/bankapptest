from django.db import models
from random import randint
from random import randint


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100)
    branch_city = models.CharField(max_length=50)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)

    def __str__(self):
        return self.branch_name


class Account(models.Model):
    acc_no = models.AutoField(primary_key=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    acc_type = models.CharField(max_length=50)
    acc_balance = models.BigIntegerField()

    def __str__(self):
        return str(self.acc_no)



    def save(self):
        if not self.acc_no:
            is_unique = False
            while not is_unique:
                acc_no = randint(10000000000, 99999999999) # 19 digits: 1, random 18 digits
                is_unique = (Account.objects.filter(acc_no=acc_no).count() == 0)
            self.acc_no = acc_no
        super(Account, self).save()