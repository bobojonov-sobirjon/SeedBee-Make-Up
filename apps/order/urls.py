from django.urls import path

from apps.order.views import CardDetailsView

urlpatterns = [
    path('card-details/', CardDetailsView.as_view(), name='card-details'),
]