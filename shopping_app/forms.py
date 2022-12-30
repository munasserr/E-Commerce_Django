
from pyexpat import model
from django import forms
from home_app.models import *
from django_countries.fields import CountryField
from shopping_app.models import *
from django_countries.widgets import CountrySelectWidget # you can use django's own ModelForm here
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


#<hr class="mb-4">
class ProductForm(forms.ModelForm):
    

    class Meta:
        model = Product
        fields = ('price',)


PAYMENT_CHOICES = (
    ('CD' , 'Credit Card'),
    ('DC' , 'Debit Card')
)



class CheckoutForm(forms.ModelForm) :

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' # this line sets your form's method to post
        self.helper.field_class = 'col-md-9' # this css class attribute will be added to all of the input fields in your form. For isntance, the input text box for "Username" will have 'col-md-9'
        self.helper.layout = Layout( # the order of the items in this layout is important
            Submit('submit', 'Place Order', css_class='ml-auto btn hvr-hover'), 
    )

    class Meta:
        model = Order
        fields = (
            'fname',
            'lname',
            'user_name',
            'email',
            'address',
            'country',
            'zip',
            'payment_option',
            'credit_card_number',
            'exp_date',
            'cvv',
        )
        widgets = {
        'fname' : forms.TextInput(attrs={'class' : 'form-control' , 'id' : 'firstName' ,'required' : 'required','name':'fname'}),
        'lname' : forms.TextInput(attrs={'class' : 'form-control' , 'id' : 'lastName','required' : 'required','name':'lname'}),
        'user_name' : forms.TextInput(attrs={'class' : 'form-control' , 'id'  : "username",'required' : 'required','name':'user_name'}),
        'email' : forms.EmailInput(attrs={'class' : 'form-control' , 'type':"email" , 'id' :"email",'required' : 'required','name':'email'}),
        'address' : forms.TextInput(attrs={'class' : 'form-control', 'type':"text" , 'id' :"address",'required' : 'required','name':'address1'}),
        # 'address2' : forms.TextInput(attrs={'class' : 'form-control', 'type':"text" , 'id' :"address2",'required' : 'required','name':'address2'}),
        'country' : CountrySelectWidget(attrs={'class' : 'form-control','required' : 'required','name':'country'}),
        'zip' : forms.NumberInput(attrs={'class' : 'form-control', 'id' :"zip",'required' : 'required','name':'zip'}),
        'payment_option' : forms.RadioSelect(choices=PAYMENT_CHOICES , attrs={'class' : 'form-control form-group custom-control custom-radio' , 'type':'radio' , 'required' : 'required','name':'payment_option'}),
        # 'name_on_card' : forms.TextInput(attrs={'class' : 'form-control', 'type':"text" , 'id' :"cc-name",'required' : 'required','name':'name_on_card'}),
        'credit_card_number' : forms.NumberInput(attrs={'class' : 'form-control', 'id' :"cc-number",'required' : 'required','name':'credit_card_number'}),
        'exp_date' : forms.DateInput(attrs={'class' : 'form-control', 'type':"date" , 'id' :"cc-expiration",'required' : 'required','name':'exp_date'}),
        'cvv' : forms.NumberInput(attrs={'class' : 'form-control', 'type':"number" , 'id' :"cc-cvv",'required' : 'required','name':'cvv'}),
        }



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields=('code',)
        widgets = {
            'code' :forms.TextInput(attrs={'class' : 'form-control' ,'placeholder' :"Enter your coupon code" ,'aria-label' : "Coupon code" })
        }   