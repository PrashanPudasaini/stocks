from django.urls import path
from users import views as user_views
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm
from .views import PasswordsChangeView, SubscriptionsPageView, PasswordsResetView, PasswordsResetConfirmView
from .views import SignUpView, ActivateAccount
from .views import PortfolioCreateView, PortfolioDetailView, PortfolioAllStocksView, PortfolioUpdateView, PortfolioDeleteView


urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('account/', views.account, name='account'),
    path('account/profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('account/password/', PasswordsChangeView.as_view(template_name='users/change-password.html'), name = 'password'),
    path('password-reset/', PasswordsResetView.as_view(template_name='users/password-reset.html'), name = 'password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordsResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name = 'password_reset_complete'),
    path('account/subscriptions/', SubscriptionsPageView.as_view(template_name='users/subscriptions.html'), name = 'subscriptions'),

    path('account/new-portfolio/', PortfolioCreateView.as_view(), name='create-new-portfolio'),
    path('account/portfolio/<slug:slug>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('account/portfolio-summary/all-stocks/', PortfolioAllStocksView.as_view(), name='portfolio-all-stocks'),
    path('account/portfolio/<slug:slug>/update/', PortfolioUpdateView.as_view(), name='portfolio-update'),
    path('account/portfolio/<slug:slug>/delete/', PortfolioDeleteView.as_view(), name='portfolio-delete'),
]
