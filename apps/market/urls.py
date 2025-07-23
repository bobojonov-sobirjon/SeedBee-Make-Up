from django.urls import path

from apps.market.views import (
	TopLevelCategoryListView, ProductListView, CommentAndReviewCreateView, ProductDetailView, ProductColorHexListView, ProductBrandListView
)

urlpatterns = [
	path('categories/', TopLevelCategoryListView.as_view(), name='top_level_category_list'),
	path('products/', ProductListView.as_view(), name='product_list'),
	path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
	path('products/review/create/', CommentAndReviewCreateView.as_view(), name='comment_and_review_create'),
	path('products/colors/', ProductColorHexListView.as_view(), name='product_color_hex_list'),
	path('products/brands/', ProductBrandListView.as_view(), name='product_brand_list'),
]

