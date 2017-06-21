from django.db import models

class Users(models.Model):
    userid = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=30)  

class Salary_type(models.Model):
    salary_typeid = models.IntegerField(primary_key=True)
    typename = models.CharField(max_length=30)
    hour_pay = models.FloatField()
    plus_pay = models.FloatField()
    base_pay = models.FloatField()                  


class People(models.Model):
    peopleid = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=30)
    nation = models.CharField(max_length=7)
    sex = models.BooleanField(default=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    date = models.DateField()
    allsalary = models.FloatField(default=0)
    ptype = models.ForeignKey(Salary_type)

class Salary(models.Model):
    salaryid = models.ForeignKey(People,primary_key=True)

    hour = models.FloatField()
    plus = models.FloatField()
    forfeit = models.FloatField()
    sub = models.FloatField() 
	

              
class Yewu(models.Model):
    yewuid = models.IntegerField(primary_key=True)
    yewupeopleid = models.ForeignKey(Users)
    
    title = models.CharField(max_length=50)
    #zhishou = models.BooleanField(default=True)
    person = models.CharField(max_length=30)
    beizhu = models.CharField(max_length=100)
    
    date = models.DateField()
    money = models.FloatField()
    ispermiss = models.BooleanField(default=False)   
    isover= models.BooleanField(default=False)   

class Card(models.Model):
        cardid = models.ForeignKey(People,primary_key=True)
        start = models.IntegerField()
        over = models.IntegerField()
        date = models.DateField()
        hours = models.IntegerField(default=0)
		    

    