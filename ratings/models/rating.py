from django.db import models
from ratings.models.category import Category
from ratings.models.rateable import Rateable

class Rating(models.Model):
    category = models.ForeignKey(Category)
    rateable = models.ForeignKey(Rateable)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    comment = models.TextField(default="Rating comment")
    

    class Meta:
        app_label = 'ratings'
