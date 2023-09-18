from django.db import models
from datetime import datetime

class subscription(models.Model):
    id = models.IntegerField(primary_key=True,null=False, verbose_name='id')
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    duration_days = models.IntegerField(default=0)
    
    def __str__(self):
        return self.description

class role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    
    def __str__(self):
        return self.name
    
class user(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(default=datetime.now())
    direction = models.CharField(max_length=100)
    user_photo = models.CharField(max_length=255)
    subscript = models.IntegerField()
    
    def __str__(self):
        self.email
    
class user_role(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    role_id = models.IntegerField()
     
    def __str__(self):
        self.user_id
        
