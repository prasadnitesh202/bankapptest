from django.db import models
from random import randint
from datetime import datetime


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

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.loan_id)


class BankUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth', default=datetime.now)

    def __str__(self):
        return str(self.name)


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    isDebit = models.BooleanField()

    def __str__(self):
        return str(self.card_id)


class Atm(models.Model):
    atm_id=models.AutoField(primary_key=True)
    city=models.CharField(max_length=50)
    latitude=models.CharField(max_length=10)
    longitude=models.CharField(max_length=10)

    def __str__(self):
        return str(self.atm_id)

class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    acc_no=models.ForeignKey(Account,on_delete=models.CASCADE)
    is_debited=models.BooleanField(default=True)
    date_time=models.DateTimeField(default=datetime.now())
    amount=models.IntegerField()
    def __str__(self):
        if(self.is_debited==True):
            return str('debited '+str(self.amount)+' from account no: '+str(self.acc_no))
        else:
            return str('credited '+str(self.amount)+' to account no: '+str(self.acc_no))
class EMI(models.Model):
    loan_id=models.ForeignKey(Loan,unique=True,on_delete=models.CASCADE,)
    interest=models.FloatField()
    installment=models.IntegerField()

    def __str__(self):
        return str(self.loan_id)

class FixedDeposit(models.Model):
    acc_no=models.ForeignKey(Account,on_delete=models.CASCADE)
    amount=models.IntegerField()
    start_date=models.DateField()
    end_date=models.DateField()
    interest=models.FloatField()

    def __str__(self):
        return str(self.acc_no)+' :amount: '+str(self.amount)
        




