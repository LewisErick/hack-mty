from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.TextField(default="Client name")
    bith_date = models.DateField(default="01/01/1970")
    city = models.TextField(default="Client city")
    country = models.TextField(default="Client country")
    mail = models.EmailField(default="client@email.com")
    user = models.OneToOneField(User)
    
    class Meta:
        app_label = 'ratings'
