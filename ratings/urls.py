from django.conf.urls import include, url
from ratings.views.rateableView import RateableDetailsView, RateableListView, RateableUpdateView
from ratings.views.baseView import BaseView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'', login_required(BaseView.as_view()), name="base"),
    url(r'^ratings/', login_required(RateableListView.as_view()), name="promotion_details"),
    url(r'^ratings/(?P<promotion_id>\d+)', login_required(RateableDetailsView.as_view()), name="promotion_list"),
    url(r'^ratings/update/(?P<promotion_id>\d+)', login_required(RateableUpdateView.as_view()), name="promotion_update"),
]
