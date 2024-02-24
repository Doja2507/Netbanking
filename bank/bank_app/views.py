from decimal import Decimal
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import FixedDeposit
from .models import UserInfo
from .models import Transaction, Payment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FixedDeposit
from .models import LoanApproval
from django.conf import settings
from django.core.mail import send_mail
from .models import LoanInfo  
from django.http import HttpResponse
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_exempt


# --------------home page--------------------------------------------------------
def my_home(request):
    # userid = request.user.id
    return render(request, "my_home.html")


# ----------------contact us---------------------------------------------------------
def contact(request):
    return render(request, "contact.html")


# -------------map--------------------------------------------------------------------
def map_view(request):
    context = {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "map.html", context)


# ------------------about us -----------------------------------------------------------
def about_us(request):
    return render(request, "about us.html")


# --------------------static data---------------------------------------------------------
def saving(request):
    return render(request, "saving.html")


def current(request):
    return render(request, "current.html")


def have(request):
    return render(request, "have.html")


def fix(request):
    return render(request, "fixed.html")


def Insurance(request):
    return render(request, "Insurance.html")


# ----------------credit card------------------------------------------
def cc(request):
    return render(request, "CC.html")


# ------------------dashboard-----------------------------------------------------------
def dashboard(request):
    userid = request.user.id
    print("id of logged in user: ", userid)
    print("result is: ", request.user.is_authenticated)
    transactions = Transaction.objects.filter(user=request.user)
    payments = []
    for x in transactions:
        p = Payment.objects.create(
            user=request.user,
            transaction_type=x.transaction_type,
            amount=x.amount,
            description=x.description,
        )
        p.save()
        payments.append(p)
    total_amount = 0
    num_payments = len(payments)
    for x in payments:
        if x.transaction_type == "deposit":
            total_amount += x.amount
        elif x.transaction_type == "withdrawal":
            total_amount -= x.amount
    context = {"data": payments, "total": total_amount, "n": num_payments}
    context["transaction"] = transactions
    return render(request, "dashboard.html", context)


# --------------login----------------------------------------------------------------
def user_login(request):
    if request.method == "POST":
        uname = request.POST["uname"]
        upass = request.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "fields cannot be empty.."
            return render(request, "login.html", context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(request, u)  # start the session
                return redirect("/dashboard/")
            else:
                context["errmsg"] = "Invalid username and password.."
                return render(request, "login.html", context)
    else:
        return render(request, "login.html")


#  ------------------logout----------------------------------------------------------
def user_logout(request):
    logout(request)
    return redirect("/my_home/")


#  -----------------register---------------------------------------------------------
def user_register(request):
    if request.method == "POST":
        uname = request.POST["uname"]
        upass = request.POST["upass"]
        ucpass = request.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "fields cannot be empty.."
            return render(request, "register.html", context)
        elif upass != ucpass:
            context["errmsg"] = "password and confirm password didn't match.."
            return render(request, "register.html", context)
        else:
            try:
                u = User.objects.create(username=uname, password=upass, email=uname)
                u.set_password(upass)  # encrypt format
                u.save()
                context["success"] = "User created successfully"
                return render(request, "register.html", context)
            except Exception:
                context["errmsg"] = "user with same username already present.."
                return render(request, "register.html", context)
    else:
        return render(request, "register.html")


# -----------------user info-------------------------------------------------------------------
def update_user_info(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        Aadhar = request.POST.get("Aadhar")
        PAN = request.POST.get("pan")
        mobile = request.POST.get("mobile")
        photo = request.FILES.get("photo")
        signature = request.FILES.get("signature")

        user_info = UserInfo.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            Aadhar=Aadhar,
            PAN=PAN,
            mobile=mobile,
            photo=photo,
            signature=signature,
        )
        return render(request, "confirmation.html", {"user_info": user_info})
    else:
        return render(request, "personal.html")


def confirmation(request):
    return render(request, "confirmation.html")


# ------------transactions----------------------------------------------------------------------
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, "transaction_list.html", {"transactions": transactions})


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    return render(request, "transaction_detail.html", {"transaction": transaction})


@login_required
def create_transaction(request):
    if request.method == "POST":
        # Process form data if submitted
        transaction_type = request.POST.get("transaction_type")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        if transaction_type and amount:
            # Create a new transaction
            Transaction.objects.create(
                user=request.user,
                transaction_type=transaction_type,
                amount=amount,
                description=description,
            )
            return redirect("transaction_list")
    else:
        return render(request, "create_transaction.html")


# ----------payment gateway-----------------------------------------------------------
def online(request):
    transactions = Transaction.objects.filter(user=request.user)
    payments = []

    for transaction in transactions:
        try:
            payment = Payment.objects.create(
                user=request.user,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
                description=transaction.description,
            )
            payments.append(payment)
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            # You can log the error or provide appropriate feedback to the user
            pass

    total_amount = sum(
        p.amount for p in payments if p.transaction_type == "deposit"
    ) - sum(p.amount for p in payments if p.transaction_type == "withdrawal")

    num_payments = len(payments)
    context = {"data": payments, "total": total_amount, "n": num_payments}
    return render(request, "payment.html", context)


# ---------------------------------------------------------------------------------------------------
@csrf_exempt
def makepayment(request):
    payments = Payment.objects.filter(user=request.user)
    context = {}
    if payments.exists():
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=("rzp_test_CoEDtyO7Q2DTce", "W39peEnk6HblY7SjLn9HqPR6")
        )

        for payment in payments:
            total_amount = payment.amount
            trans_id = payment.razorpay_payment_id

            # Create data for Razorpay order
            data = {
                "amount": total_amount * 100,  # Amount is in paisa
                "currency": "INR",
                "receipt": trans_id,
            }

            try:
                # Create a Razorpay order
                order = client.order.create(data=data)
                context["data"] = order
            except razorpay.errors.RazorpayError as e:
                # Handle any exceptions (e.g., network errors, invalid data)
                context["error_message"] = str(e)

    return render(request, "pay.html", context)

def status_view(request):
    return render(request, 'status.html')


# --------------loan-info-------------------------------------------------------
class LoanApplicationView(SuccessMessageMixin, View):
    def get(self, request):
        return render(request, "loan_application.html")

   
    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        nominee_name = request.POST.get("nominee_name")
        loan_amount = Decimal(request.POST.get("loan_amount"))
        reason_for_loan = request.POST.get("reason_for_loan")
        loan_date = request.POST.get("loan_date")
        monthly_salary = Decimal(request.POST.get("monthly_salary"))
        loan_type = request.POST.get("loan_type")
        term_months = int(request.POST.get("term_months"))

        with transaction.atomic():
            loan_info = LoanInfo.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                nominee_name=nominee_name,
                loan_amount=loan_amount,
                reason_for_loan=reason_for_loan,
                loan_date=loan_date,
                monthly_salary=monthly_salary,
                loan_type=loan_type,
                term_months=term_months,
            )
            messages.success(request, "Loan application submitted successfully.")
            return redirect('loan_confirmation')


class LoanConfirmationView(View):
    def get(self, request):
        latest_loan = LoanInfo.objects.last()
        context = {
            "loan": latest_loan,
        }
        return render(request, "loan_confirmation.html", context)


class CreateLoanApprovalView(View):
    def get(self, request):
        latest_loan = LoanInfo.objects.all( )
        context = {
            "loan_approval": LoanApproval.objects.create(user=request.user,
                loan_type=latest_loan.loan_type,
                amount=latest_loan.loan_amount,
                duration_months=latest_loan.term_months,
            ),
        }
        return render(request, "loan_approval_confirmation.html", context)


class CalculateEMIView(View):
    def get(self, request):
        return render(request, "calculate_emi.html")

    @login_required
    def post(self, request):
        loan_type = request.POST.get("loan_type")
        loan_amount = Decimal(request.POST.get("loan_amount"))
        term_months = int(request.POST.get("term_months"))
        interest_rates = {
            "personal": 10.0,
            "home": 8.0,
            "vehicle": 9.0,
            "property": 12.0,
        }

        interest_rate = interest_rates.get(loan_type, 0)
        r = Decimal(interest_rate) / 100 / 12
        n = term_months
        emi = (loan_amount * r * (Decimal(1) + r) ** n) / (
            (Decimal(1) + r) ** n - Decimal(1)
        )
        context = {"emi": emi}
        return render(request, "emi_details.html", context)

class LoanDetailsView(View):
    def get(self, request):
        loans = LoanInfo.objects.filter(user=request.user)
        for loan in loans:
            # Assuming loan_amount, loan_type, and term_months are attributes of LoanInfo
            emi = loan.calculate_emi(loan.loan_amount, loan.loan_type, loan.term_months)
            loan.emi = emi
        context = {"loans": loans}
        return render(request, "loan_details.html", context)



class LoanApprovalConfirmationView(View):
    def get(self, request):
        loan_approvals = LoanApproval.objects.filter(user=request.user)
        context = {"loan_approvals": loan_approvals}
        return render(request, "loan_approval_confirmation.html", context)


# ---------------FD---------------------------------------------------------------
@login_required
def create_fixed_deposit(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        duration_months = request.POST["duration_months"]
        interest_rate = request.POST.get(
            "interest_rate", 9
        )  # Default to 9 if not provided

        fixed_deposit = FixedDeposit.objects.create(
            user=request.user,
            amount=amount,
            duration_months=duration_months,
            interest_rate=interest_rate,
        )
        return redirect("fd_save")
    return render(request, "FD.html")


@login_required
def fd_save(request):
    fixed_deposits = FixedDeposit.objects.filter(user=request.user)
    return render(request, "FD_success.html", {"fixed_deposits": fixed_deposits})


@login_required
def deposit(request):
    fixed_deposits = FixedDeposit.objects.filter(user=request.user)
    for deposit in fixed_deposits:
        deposit.total_amount = deposit.calculate_total_amount()
    return render(request, "FD_save.html", {"fixed_deposits": fixed_deposits})

# ----------------send mail-----------------------------------------------
def send_approval_email(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')

        try:
            loan = LoanInfo.objects.get(id=loan_id)
        except LoanInfo.DoesNotExist:
            return HttpResponse('Loan not found', status=404)


        sender_email = 'dkjadhav2507@gmail.com'  # Set the sender's email address
        recipient_email = 'dkjadhav2507@gmail.com' 
        # Compose the email message
        subject = 'Loan Approval'
        message = f'''
        Dear Customer,

        We are pleased to inform you that your loan application with the following details has been approved:

        Loan ID: {loan.id}
        First Name: {loan.first_name}
        Last Name: {loan.last_name}
        Nominee Name: {loan.nominee_name}
        Loan Amount: {loan.loan_amount}
        Reason for Loan: {loan.reason_for_loan}
        Loan Date: {loan.loan_date}
        Monthly Salary: {loan.monthly_salary}
        Loan Type: {loan.loan_type}
        Term (in months): {loan.term_months}

        Thank you for choosing our services.

        Regards,
        Our Bank
        '''

        # Send the email
        try:
            send_mail(subject, message, sender_email, [recipient_email])
            context = {'loan': loan}
            return render(request, 'loan_approval_confirmation.html', context)
        except Exception as e:
            return HttpResponse('Error sending email: ' + str(e), status=500)
    else:
        return HttpResponse('Invalid request', status=400)


# ---------------------payment--------------------------
def loan_online(request):
    Loan_info=LoanInfo.objects.filter(user=request.user)
    payments=[]
    for x in Loan_info:
        l=LoanApproval.objects.create(user=request.user,loan_type=x.loan_type,loan_amount=x.loan_amount,term_months=x.term_months)
        l.save()
        payments.append(l)
    total_amount=x.loan_amount-3000     
    num_payments = len(payments)
    context = {"data": payments, "total": total_amount, "n": num_payments}
    return render(request, "loanpayment.html", context)

def loanpayment(request):
    payments = LoanApproval.objects.filter(user=request.user)
    context = {}
    if payments.exists():
        client = razorpay.Client(
            auth=("rzp_test_CoEDtyO7Q2DTce", "W39peEnk6HblY7SjLn9HqPR6")
        )
        for x in payments:
            total_amount = 3000
            trans_id = x.razorpay_payment_id

            data = {
                "amount": total_amount * 100,  # Amount is in paisa
                "currency": "INR",
                "receipt": trans_id,
            }
            pay = client.order.create(data=data)
            context["data"] = pay

    return render(request, "pay.html", context)


