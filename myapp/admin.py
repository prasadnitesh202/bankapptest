from django.contrib import admin
from .models import Branch,Account,Loan,Atm


admin.site.register(Branch)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(Atm)