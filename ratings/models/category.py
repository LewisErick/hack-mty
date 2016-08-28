from django.db import models

class Category(models.Model):
	name = models.TextField(default="CategoryName")

	class Meta:
		app_label = 'ratings'