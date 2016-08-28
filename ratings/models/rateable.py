from django.db import models
from ratings.models.category import Category
from django.core.validators import RegexValidator

class Rateable(models.Model):
	name = models.TextField(default="Rateable name")
	category = models.ForeignKey(Category)
	address = models.TextField(default="Rateable address.")
	city = models.TextField(default="Rateable city.")
	description = models.TextField(default="Description.")
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True) # validators should be a list
	average = models.IntegerField(min=0, max=100, default=0)

	class Meta:
		app_label = 'ratings'
