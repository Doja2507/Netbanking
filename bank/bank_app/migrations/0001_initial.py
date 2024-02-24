# Generated by Django 4.2.5 on 2024-02-21 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('1', 'Maharashtra'), ('2', 'Goa'), ('3', 'Gujrat'), ('4', 'Rajsthan'), ('5', 'Andra Pradesh'), ('6', 'Kerala'), ('7', 'Tamil Nadu'), ('8', 'Delhi'), ('9', 'Madhya Pradesh'), ('10', 'Uttar Pradesh')], max_length=2)),
                ('zipcode', models.IntegerField()),
                ('Aadhar', models.BigIntegerField()),
                ('PAN', models.BigIntegerField()),
                ('mobile', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='user_photos/')),
                ('signature', models.FileField(upload_to='user_signatures/')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], max_length=20)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], max_length=20)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('nominee_name', models.CharField(max_length=100)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reason_for_loan', models.TextField()),
                ('loan_date', models.DateField()),
                ('monthly_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_type', models.CharField(choices=[('personal', 'Personal Loan'), ('home', 'Home Loan'), ('vehicle', 'Vehicle Loan'), ('property', 'Property Loan')], max_length=20)),
                ('term_months', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.CharField(choices=[('personal', 'Personal Loan'), ('home', 'Home Loan'), ('vehicle', 'Vehicle Loan'), ('property', 'Property Loan')], max_length=20)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('term_months', models.IntegerField()),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FixedDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_months', models.IntegerField()),
                ('interest_rate', models.FloatField(default=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
