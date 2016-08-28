from django.db import models

class Client(models.Model):
    name = models.TextField(default="Client name")
    bith_date = models.DateField(default="01/01/1970")
    city = models.TextField(default="Client city")
    country = models.TextField(default="Client country")
    mail = models.EmailField(default="client@email.com")
    
    class Meta:
        app_label = 'ratings'
