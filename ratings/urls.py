from django.conf.urls import include, url
from ratings.views.rateableView import RateableDetailsView, RateableListView, RateableUpdateView
from ratings.views.baseView import BaseView

urlpatterns = [
	url(r'^base/', BaseView.as_view(), name="base"),
    url(r'^promotions/', RateableListView.as_view(), "promotion_details"),
    url(r'^promotions/(?P<promotion_id>\d+)', RateableDetailsView.as_view(), "promotion_list"),
    url(r'^promotions/update/(?P<promotion_id>\d+)', RateableUpdateView.as_view(), "promotion_update"),
]