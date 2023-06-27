from django.db import models

# Create your models here.
class Users(models.Model):
    Name=models.CharField(max_length=100)
    Aadhar=models.CharField(max_length=12)
    Mobile=models.CharField(max_length=10)
    Email=models.EmailField(max_length=255)
    Date_Of_Birth=models.DateField()
    Account_Number=models.CharField(max_length=20)
    IFSC=models.CharField(max_length=12)
    Bank_Name=models.CharField(max_length=100)
    User_ID=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    MPIN=models.CharField(max_length=6)
    Status=models.CharField(max_length=20)
    Balance=models.IntegerField()
    Unique_Key=models.CharField(max_length=13,default='qwertyuiopasd')
    Active_Status=models.BooleanField(default=False)

class Payments(models.Model):
    Sender=models.CharField(max_length=100)
    Reciever=models.CharField(max_length=100)
    Amount=models.IntegerField()
    Date_time=models.DateTimeField()
    Remarks=models.TextField()
    Reference_Number=models.CharField(max_length=20)
    Payment_Status=models.CharField(max_length=20)

class MESSAGES(models.Model):
    From=models.CharField(max_length=100)
    To=models.CharField(max_length=100)
    Message=models.TextField()
    Date_time=models.DateTimeField()

class Queries(models.Model):
    From=models.CharField(max_length=100)
    Query=models.TextField()
    Date_time=models.DateTimeField()
    Query_Status=models.CharField(max_length=20)