from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




BUSINESSES = (
    ('', 'Sole Propriatorship'),
    ('P', 'Partnarship'),
    ('LL', 'Limited Liability'),
    ('O', 'Others')
)

AGES = (
    ('', 'Less than 1 Month'),
    ('1', '1 - 3 Months'),
    ('2', '4 - 6 Months'),
    ('3', '7 - 12 Months'),
    ('4', '1 - 2 Years'),
    ('5', '2+ Years')
)

INDUSRY = (
    ('', 'Manufacturing'),
    ('A', 'Clothing'),
    ('B', 'Technology'),
    ('C', 'Internet'),
    ('D', 'Engineering/Design'),
    ('E', 'Retails'),
    ('F', 'Uknown/Other'),
    ('G', 'Computers/Electronics'),
    ('H', 'Agriculture'),
    ('I', 'Printing'),
    ('J', 'Insurance'),
    ('K', 'Education'),
    ('L', 'Health'),
    ('M', 'Services'),
    ('N', 'Fast Moving Consumer Goods'),
    ('O', 'Restaurant'),
    ('P', 'Food'),
    ('Q', 'Transport'),
    ('R', 'Property'),
    ('S', 'Real Estate'),
    ('T', 'Wholesale'),
    ('U', 'Hospitality')
)

REVENUE = (
     ('', 'KES 0 to KES 50,000'),
    ('A', 'KES 50,000 to KES 100,000'),
    ('B', 'KES 50,000 to KES 100,000'),
    ('C', 'KES 100,000 to KES 200,000'),
    ('D', 'KES 200,000 to KES 500,000'),
    ('E', 'KES 500,000 to KES 1 million'),
    ('F', 'KES 1 million to KES 2 million'),
    ('G', 'KES 2 million to KES 5 million'),
    ('H', 'KES 5 million +')
)

MPESA = (
    ('', 'NO'),
    ('1', 'YES')
)

AMOUNTS = (
    ('', 'Less than Kshs 10,000'),
    ('1', 'Kshs 10,000 - Kshs 50,000'),
    ('2', 'Kshs 50,001 - Kshs 150,000'),
    ('3', 'Kshs 150,001 - Kshs 500,000'),
    ('4', 'Kshs 500,001 - Kshs 1,000,000')
)

USES = (
    ('', 'Inventory/Stock purchase'),
    ('1', 'Equipment/Machinery'),
    ('2', 'Cashflow/Working Capital'),
    ('3', 'Refinancing a loan'),
    ('4', 'Expansion'),
    ('5', 'Other')
)

MONTHS = (
    ('', '2 Months'),
    ('1', '3 Months'),
    ('2', '6 Months'),
    ('3', '9 Months'),
    ('4', '12 Months')
)


SOCIALS = (
    ('', 'Google Search'),
    ('1', 'Facebook'),
    ('2', 'An SME Pezesha has already funded'),
    ('3', 'Referred by an employee of Pezesha'),
    ('4', 'Recommendation from a friend'),
    ('5', 'I am part of a program that recommended it'),
    ('6', 'News'),
    ('7', 'Other')
)

class PersonalForm(forms.Form):
    full_name = forms.CharField(label='Full Name On National ID', widget=forms.TextInput())
    national_id = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))


class BusinessForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput())
    specific_location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg. Nairobi CBD at Telcom Towers'}))
    type_of_business = forms.ChoiceField(label='Type of Business Registration?', choices=BUSINESSES)
    age_of_business = forms.ChoiceField( label='How old is your business?', choices=AGES)
    bsn_industry = forms.ChoiceField(label='Industry of Business?', choices=INDUSRY)
    company_reg = forms.CharField(label='Company Registration No or Equivalent', widget=forms.TextInput())
    est_revenue = forms.ChoiceField(label='Estimated Yearly Revenue? (KES)', choices=REVENUE)
    comp_site = forms.CharField(label='Company Website/Social Media (Optional)', widget=forms.TextInput()) 
    mpesa = forms.ChoiceField(label='Mpesa\Till No Business Payments Accepted?', choices=MPESA)

class NeedsForm(forms.Form):
    kra_pin = forms.CharField(label = 'Personal or Business KRA Pin (For verification)', widget=forms.TextInput())
    amount_needed = forms.ChoiceField(label = 'How much do you need? (KSHS)', choices=AMOUNTS)
    funds_for = forms.ChoiceField(label = 'What will you use the funds for?', choices=USES)
    months_for = forms.ChoiceField(label = 'In how many months will you pay back the loan?', choices=MONTHS)
    about_us = forms.ChoiceField(label = 'How did you hear about our SME program?', choices=SOCIALS)
    agreed = forms.BooleanField(required=False, label='I agree with the terms and conditions')

class CustomCheckbox(Field):
    template = 'custom_checkbox.html'

class CustomBusinessFieldForm(BusinessForm):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-4 mb-0'),
                Column('specific_location', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
           
            Row(
                Column('type_of_business', css_class='form-group col-md-4 mb-0'),
                Column('age_of_business', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('bsn_industry', css_class='form-group col-md-4 mb-0'),
                Column('est_revenue', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),

            Row(
                Column('company_reg', css_class='form-group col-md-4 mb-0'),
                Column('comp_site', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

              Row(
                Column('mpesa', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            CustomCheckbox('check_me_out'),
            Submit('submit', 'Next')
        )


class CustomFieldForm(PersonalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                   
               Row(
                Column('full_name', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
           
            Row(
                Column('national_id', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),


             Row(
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

     
            Submit('submit', 'Next')
        )

class CustomNeedsFieldForm(NeedsForm):
     def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                    
                 Row(
                Column('kra_pin', css_class='form-group col-md-4 mb-0'),
                Column('amount_needed', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
           
            Row(
                Column('funds_for', css_class='form-group col-md-8 mb-0'),
                
                css_class='form-row'
            ),

            Row(
                Column('months_for', css_class='form-group col-md-4 mb-0'),
                Column('about_us', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
                
            ),

    

            'agreed',
            Submit('submit', 'Submit Application')
        )
