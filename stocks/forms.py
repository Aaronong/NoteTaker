from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from models import ParentOrder

def validate_order_quantity(value):
    if value <= 0:
        raise ValidationError(
            _('Please enter an integer greater than zero.'),
            code='negative'
        )

class ParentOrderForm(forms.ModelForm):

    BUY_OR_SELL_CHOICE = (
        (True, 'Sell'),
    )

    STOCK_CHOICE = (
        ('ACME ETF', 'ACME ETF'),
    )

    is_sell = forms.ChoiceField(label="Buy or Sell?", choices=BUY_OR_SELL_CHOICE, required=True, 
        widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label='Quantity', required=True,
        error_messages = {'required': _('Enter a whole number.')},
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock_type = forms.ChoiceField(label="Stock Type", choices=STOCK_CHOICE, required=True, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ParentOrder
        fields = ('is_sell', 'quantity', 'stock_type')

class PauseResumeForm(forms.ModelForm):

    status = forms.CharField(widget = forms.HiddenInput(), required = True)

    class Meta:
        model = ParentOrder
        fields = ('status',)