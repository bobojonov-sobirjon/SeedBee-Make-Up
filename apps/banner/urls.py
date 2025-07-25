from django.urls import path

from apps.banner.views import (
	BannerListView, PartnerListView, AdvertisementListView, BlogListView, 
	BlogDetailView,
)

urlpatterns = [
	path('banners/', BannerListView.as_view(), name='banner-list'),
	path('partners/', PartnerListView.as_view(), name='partner-list'),
	path('advertisements/', AdvertisementListView.as_view(), name='advertisement-list'),
	path('blogs/', BlogListView.as_view(), name='blog-list'),
	path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]