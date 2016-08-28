from django.views.generic.base import TemplateView
from ratings.models.rateable import Rateable

class BaseView(TemplateView):
	template_name = 'index.html'
	model = Rateable