from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
import requests

# User Information Model
class UserInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    STATE_CHOICES = [
        ("1", "Maharashtra"),
        ("2", "Goa"),
        ("3", "Gujrat"),
        ("4", "Rajsthan"),
        ("5", "Andra Pradesh"),
        ("6", "Kerala"),
        ("7", "Tamil Nadu"),
        ("8", "Delhi"),
        ("9", "Madhya Pradesh"),
        ("10", "Uttar Pradesh"),
    ]
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zipcode = models.IntegerField()
    Aadhar = models.BigIntegerField()
    PAN = models.BigIntegerField()
    mobile = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='user_photos/')
    signature = models.FileField(upload_to='user_signatures/')

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

# Payment Model
class Payment(models.Model):
    TRANSACTION_TYPES = (
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)


# Fixed Deposit Model
class FixedDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    interest_rate = models.FloatField(default=9)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_amount(self):
        interest_rate_decimal = Decimal(str(self.interest_rate))
        total_amount = self.amount + (
            self.amount * interest_rate_decimal * self.duration_months / 12 / 100
        )
        return total_amount
# loan Information model
# class LoanInfo(models.Model):
#     LOAN_TYPES = [
#         ("personal", "Personal Loan"),
#         ("home", "Home Loan"),
#         ("vehicle", "Vehicle Loan"),
#         ("property", "Property Loan"),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     nominee_name = models.CharField(max_length=100)
#     loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     reason_for_loan = models.TextField()
#     loan_date = models.DateField()
#     monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
#     loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
#     term_months = models.IntegerField()
    
#     def calculate_emi(self):
#         interest_rates = {
#             "personal": 10.0,  # Example interest rates (adjust as needed)
#             "home": 8.0,
#             "vehicle": 9.0,
#             "property": 12.0,
#         }
        
#         interest_rate = interest_rates.get(self.loan_type, 0)
#         r = Decimal(interest_rate) / 100 / 12
#         n = self.term_months
#         emi = (self.loan_amount * r * (Decimal(1) + r) ** n) / ((Decimal(1) + r) ** n - Decimal(1))
#         return emi
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.get_loan_type_display()}"

# # Loan Approval Model
# class LoanApproval(models.Model):
#     LOAN_TYPES = (
#         ("personal", "Personal Loan"),
#         ("home", "Home Loan"),
#         ("vehicle", "Vehicle Loan"),
#         ("property", "Property Loan"),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey referencing the User model
#     loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
#     loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     term_months = models.IntegerField()
#     razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

#     def calculate_emi(self):
#         interest_rates = {
#             "personal": 10.0,
#             "home": 8.0,
#             "vehicle": 9.0,
#             "property": 12.0,
#         }
#         interest_rate = interest_rates.get(self.loan_type, 0)
#         r = Decimal(interest_rate) / 100 / 12
#         n = self.term_months
#         emi = (self.loan_amount * r * (Decimal(1) + r) ** n) / ((Decimal(1) + r) ** n - Decimal(1))
#         return round(emi, 2)

#     def __str__(self):
#         return f"{self.user.username}'s {self.get_loan_type_display()} Approval - Amount: {self.loan_amount}, Duration: {self.term_months} months"
    
LOAN_TYPES = (
    ("personal", "Personal Loan"),
    ("home", "Home Loan"),
    ("vehicle", "Vehicle Loan"),
    ("property", "Property Loan"),
)


class LoanInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nominee_name = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason_for_loan = models.TextField()
    loan_date = models.DateField()
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=20)
    term_months = models.IntegerField()

    @staticmethod
    def calculate_emi(loan_amount, loan_type, term_months):
        interest_rates = {"personal": 10.0, "home": 8.0, "vehicle": 9.0, "property": 12.0}
        interest_rate = interest_rates.get(loan_type, 0)
        r = Decimal(interest_rate) / 100 / 12
        n = term_months
        emi = (loan_amount * r * (Decimal(1) + r) ** n) / ((Decimal(1) + r) ** n - Decimal(1))
        return round(emi, 2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_loan_type_display()}"


class LoanApproval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=20)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.IntegerField()
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def calculate_emi(loan_amount, loan_type, term_months):
        interest_rates = {"personal": 10.0, "home": 8.0, "vehicle": 9.0, "property": 12.0}
        interest_rate = interest_rates.get(loan_type, 0)
        r = Decimal(interest_rate) / 100 / 12
        n = term_months
        emi = (loan_amount * r * (Decimal(1) + r) ** n) / ((Decimal(1) + r) ** n - Decimal(1))
        return round(emi, 2)

    def __str__(self):
        return f"{self.user.username}'s {self.get_loan_type_display()} Approval - Amount: {self.loan_amount}, Duration: {self.term_months} months" 

 





