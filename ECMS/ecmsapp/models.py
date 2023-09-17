from django.db import models


# Create your models here.
# --------------- User Account -----------------
class Users(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=7)
    tell = models.CharField(max_length=15)
    username = models.CharField(max_length=15)   
    password = models.CharField(max_length=15)
    active = models.BooleanField(default=True) # True if we are active Else False to disable
    status = models.IntegerField(default=0) # status 0 means this one is active while 1 = inactive user

# --------------- House Table -----------------
class House(models.Model):
    district =models.CharField(max_length=15)
    type = models.CharField(max_length=15)
    houseno = models.CharField(max_length=25)
    status = models.IntegerField(default=0) # default 0 is reserved for Active while 1 is reserved for Deleted


class Golden(models.Model):
    district =models.CharField(max_length=15)
    type = models.CharField(max_length=15)
    houseno = models.CharField(max_length=25)
    status = models.IntegerField(default=0) # default 0 is reserved for Active while 1 is reserved for Deleted

# --------------- Renter Table -----------------
class Renter(models.Model):
    name = models.CharField(max_length=25)
    tell = models.CharField(max_length=15)
    martial_status = models.CharField(max_length=15)
    status = models.IntegerField(default=0) # default 0 is Active while 1 is deleted

# --------------- Enviroment Table -----------------
class Enviroment(models.Model):
    register_date = models.DateField()
    status = models.IntegerField(default=0) # default 0 is Active and 1 is deactivated
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)

# --------------- Service Table -----------------
class Service(models.Model):
    date = models.DateField()
    status = models.IntegerField(default=0) # default 0 is active and 1 is deactivated
    enviroment = models.ForeignKey(Enviroment,on_delete=models.CASCADE)
    process = models.CharField(max_length=15,default='Un-Paid')

# --------------- Transaction Table -----------------
class Transaction(models.Model):
    account = models.CharField(max_length=10)
    price = models.IntegerField()
    date = models.DateField()
    status = models.IntegerField(default=0) # default 0 is active and 1 is deactivated
    service = models.ForeignKey(Service,on_delete= models.CASCADE)

class userLoggers(models.Model):
    level = models.CharField(max_length=10)
    message = models.TextField()
    device = models.TextField(null=True)
    logger_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.logger_name}: {self.message}'