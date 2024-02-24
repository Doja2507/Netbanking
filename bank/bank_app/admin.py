from django.contrib import admin
from .models import UserInfo, Transaction, Payment, LoanInfo, FixedDeposit, LoanApproval

# Register your models with the admin site
admin.site.register(UserInfo)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(LoanInfo)
admin.site.register(FixedDeposit)
admin.site.register(LoanApproval)
