from django.conf.urls import include, url
from promotions.views.promotionView import PromotionDetailsView, PromotionListView, PromotionUpdateView

urlpatterns = [
    url(r'^promotions/$', PromotionDetailsView.as_view(), "promotions_list"),
    url(r'^promotions/(?P<promotion_id>\d+)', PromotionListView.as_view(), "promotion")
    url(r'^promotions/update/(?P<promotion_id>\d+)', PromotionUpdateView.as_view(), "promotion")
]
