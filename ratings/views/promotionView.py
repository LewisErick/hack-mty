from django.views.generic.base import DetailView, ListView, UpdateView

class RateableDetailsView(views.DetailsView):
	template_name = 'rateables/details.html'
    model = Rateable

class RateableListView(views.ListView):
	template_name = 'rateables/search.html'
    model = Rateable

class RateableListView(views.UpdateView):
	template_name = 'rateables/edit.html'
    model = Rateable