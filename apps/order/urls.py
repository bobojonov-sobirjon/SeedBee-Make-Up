from django.urls import path

from apps.order.views import CardDetailsView, CardVerifyCodeView, CardVerifyView, OrderCreateView

urlpatterns = [
    path('card-details/', CardDetailsView.as_view(), name='card-details'),
    path('card-verify-code/', CardVerifyCodeView.as_view(), name='card-verify-code'),
    path('card-verify/', CardVerifyView.as_view(), name='card-verify'),
    path('order/', OrderCreateView.as_view(), name='order-create'),
]