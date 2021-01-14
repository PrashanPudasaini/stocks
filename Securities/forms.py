from django.forms import ModelForm, TextInput
from .models import Stock
from users.models import Portfolio
from django import forms
from django.forms import modelformset_factory

class StockSearchForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol']
        widgets = {
            'symbol': TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Search Symbol'})
}
    def __init__(self, *args, **kwargs):
        super(StockSearchForm, self).__init__(*args, **kwargs)
        self.fields['symbol'].label = ''

class AddToPortfolio(forms.ModelForm):
    selected = forms.BooleanField()

    class Meta:
        model = Portfolio
        fields = ['portfolio_name', 'slug']

    def __init__(self, *args, **kwargs):
        super(AddToPortfolio, self).__init__(*args, **kwargs)
        self.fields['portfolio_name'].label = ''
        self.fields['portfolio_name'].widget.attrs['readonly'] = True
        self.fields['slug'].label = ''
        self.fields['slug'].widget.attrs['readonly'] = True

AddToPortfolioFormSet = modelformset_factory(Portfolio, form = AddToPortfolio, fields = ('portfolio_name', 'slug',), extra = 0)
add_to_portfolio = AddToPortfolioFormSet()
