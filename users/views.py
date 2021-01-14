from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordChangingForm, PasswordResettingForm, PasswordResetConfirmingForm
from django.contrib.auth.decorators import login_required
from Securities.forms import StockSearchForm, AddToPortfolioFormSet, AddToPortfolio
from .forms import PortfolioCreateForm, PortfolioUpdateForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm, PasswordResetView, PasswordResetForm, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.views.generic import View, UpdateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Portfolio
from django.urls import reverse

class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till email is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Rupy Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('An email with an account activation link has been sent to your email. Please click on the link to complete registration.'))
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been verified.'))
            return redirect('profile')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')

def account(request):
    return redirect('profile')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) #ADD default_app_config = 'users.apps.UsersConfig' to __init__.py is USER HAS NO PROFILE
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'stock_search_form': StockSearchForm()
    }
    return render(request, 'users/profile.html', context)

class PasswordsChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('profile')
    success_message = f'You password has been updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        return context

class SubscriptionsPageView(LoginRequiredMixin, TemplateView):
    template_name = "users/subscriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        return context

class PasswordsResetView(SuccessMessageMixin, PasswordResetView):
    form_class = PasswordResettingForm
    success_url = reverse_lazy('login')
    success_message = f'If your email exists in our database, you will receive an email with a password recovery link. If you do not see the email, please check your spam folder.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        return context

class PasswordsResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = PasswordResetConfirmingForm
    success_url = reverse_lazy('login')
    success_message = f'You password has been reset. You can now log in.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        return context

class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    fields = ['portfolio_name']

    def form_valid(self, form):
        form.instance.portfolio_author = self.request.user
        return super().form_valid(form)

class PortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    fields = ['portfolio_name']
    template_name = 'users/stock_portfolio_detail.html'
    portfolio_update_form = PortfolioUpdateForm

    def form_valid(self, form):
        form.instance.portfolio_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        portfolio = self.get_object()
        if self.request.user == portfolio.portfolio_author:
            return True
        else:
            return False

from django.shortcuts import get_object_or_404
from Securities.models import Stock

class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'users/stock_portfolio_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()    #stock search form
        context['portfolio_create_form'] = PortfolioCreateForm()    #portfolio create form
        if self.request.user.is_active:
            context['portfolio_list'] = Portfolio.objects.filter(portfolio_author=self.request.user)    #portfolio list for navigation
        context['portfolio_update_form'] = PortfolioUpdateForm(instance = self.object)      #portfolio update form
        detail_view = get_object_or_404(Portfolio, slug = self.kwargs['slug'])  # print all symbols in each portfolio
        if self.request.user.is_active:
            portfolio_queryset = Portfolio.objects.filter(portfolio_author=self.request.user)
            portfolio = portfolio_queryset.get(portfolio_name = detail_view)
            symbols = portfolio.portfolio_symbols.all()
            context['portfolio_symbols_list'] = symbols

        if self.request.user.is_active: #Portfolio Form sets
            context['add_to_portfolio'] = AddToPortfolioFormSet(queryset = Portfolio.objects.filter(portfolio_author=self.request.user))


        is_watching = False
        add_remove_action_list = []
        portfolio_queryset = Portfolio.objects.filter(portfolio_author = self.request.user)
        for portfolio in portfolio_queryset:
            all_symbols_list = portfolio.portfolio_symbols.all().values_list('symbol', flat = True)
            if 'MFA' in all_symbols_list:
                is_watching = True
                action = "REMOVE"
            else:
                action = "ADD"
            add_remove_action_list.append(action)


        context['add_remove_action_list'] = add_remove_action_list
        context['is_watching'] = is_watching

        return context


class PortfolioAllStocksView(LoginRequiredMixin, TemplateView):
    model = Portfolio
    template_name = 'users/stock_portfolio_all_stocks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()    #stock search form
        context['portfolio_create_form'] = PortfolioCreateForm()    #portfolio create form
        if self.request.user.is_active:
            context['portfolio_list'] = Portfolio.objects.filter(portfolio_author=self.request.user)    #portfolio list for navigation
        context['portfolio_update_form'] = PortfolioUpdateForm()      #portfolio update form

        if self.request.user.is_active:
            portfolio_qset = Portfolio.objects.filter(portfolio_author=self.request.user)
            context['portfolio_qset'] = portfolio_qset

        return context

class PortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        context['portfolio_create_form'] = PortfolioCreateForm()
        context['portfolio_update_form'] = PortfolioUpdateForm()
        if self.request.user.is_active:
            context['portfolio_list'] = Portfolio.objects.filter(portfolio_author=self.request.user)
        return context

    def test_func(self):
        portfolio = self.get_object()
        if self.request.user == portfolio.portfolio_author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('stock-most-popular')
