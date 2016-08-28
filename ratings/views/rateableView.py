from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from ratings.models.rateable import Rateable

class RateableDetailsView(DetailView):
	template_name = 'rateables/details.html'
	model = Rateable

class RateableListView(ListView):
	template_name = 'rateables/search.html'
	model = Rateable

class RateableUpdateView(UpdateView):
	template_name = 'rateables/edit.html'
	model = Rateable