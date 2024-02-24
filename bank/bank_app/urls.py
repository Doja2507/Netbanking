from django.urls import path
from bank_app import views
urlpatterns = [
    # Home, About Us, and Contact
    path("my_home/", views.my_home, name="my_home"),
    path("about_us/", views.about_us, name="about_us"),
    path("contact/", views.contact, name="contact"),
    
    # Authentication
    path("login_page/", views.user_login, name="login_page"),
    path("logout_page/", views.user_logout, name="logout_page"),
    path("register_page/", views.user_register, name="register_page"),
    
    # Dashboard and User Info
    path("dashboard/", views.dashboard, name="dashboard"),
    path('update/', views.update_user_info, name='update_user_info'),
    path('confirmation/', views.confirmation, name='confirmation'),
    # Loans and Transactions
    path('loan_application/', views.LoanApplicationView.as_view(), name='loan_application'),
    path('loan_confirmation/',views.LoanConfirmationView.as_view(), name='loan_confirmation'),
    path("create_loan_approval/", views.CreateLoanApprovalView.as_view(), name="create_loan_approval"),
    path("calculate_emi/", views.CalculateEMIView.as_view(), name="calculate_emi"),
    path("loan_details/", views.LoanDetailsView.as_view(), name="loan_details"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/create/", views.create_transaction, name="create_transaction"),
    path("transactions/<int:transaction_id>/", views.transaction_detail, name="transaction_detail"),
    
    # Payments
    path("makepayment/", views.makepayment, name="makepayment"),
    path("onlinepayment/", views.online, name="onlinepayment"),
    path('status/', views.status_view, name='status'),
    path('loan/', views.loan_online, name='loan_online'),
    path('payment/', views.loanpayment, name='loanpayment'),
    
    # Fixed Deposits
    path("create_fd/", views.create_fixed_deposit, name="create_fd"),
    path("fd_save/", views.fd_save, name="fd_save"),
    path("list/", views.deposit, name="fixed_deposit_list"),
    
    # Other Pages
    path("map/", views.map_view, name="map"),
    path("saving/", views.saving, name="saving"),
    path("current/", views.current, name="current"),
    path("have/", views.have, name="have"),
    path("fix/", views.fix, name="fix"),
    path("insurance/", views.Insurance, name="insurance"),
    path("cc/", views.cc, name="credit_card"),
    path('send-approval-email/', views.send_approval_email, name='send_approval_email'),
    # path('convert_currency/', views.convert_currency, name='convert_currency'),    
]
