from django.urls import path

from apps.accounts.views import (
	UserSignupView,
	CustomAuthTokenView,
	CustomUserDetailView,
	CustomUserView,
	PasswordUpdateView,
)

urlpatterns = [
	path('signup/', UserSignupView.as_view(), name='signup'),
	path('signin/', CustomAuthTokenView.as_view(), name='signin'),
	path('user-detail/', CustomUserDetailView.as_view(), name='user-detail'),
	path('user/<int:id>/', CustomUserView.as_view(), name='user-by-id'),
	path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
]