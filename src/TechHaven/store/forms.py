from typing import Any
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
import re
from .models import Customer, Coupon
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
User = get_user_model()

class CouponForm(forms.Form):
    code = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'maxlength': '100', 'placeholder': 'Add Coupon code:'})
    )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')

        try:
            coupon = Coupon.objects.get(code=code)

            if coupon.is_expired():
                raise forms.ValidationError('This coupon has expired or is invalid.')

        except Coupon.DoesNotExist:
            raise forms.ValidationError('Invalid coupon code.')

        return code



class SixDigitForm(forms.Form):
    six_digit_number = forms.CharField(
        label='Six Digit Number',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'maxlength': '6'})
    )

    def clean_six_digit_number(self):
        value = self.cleaned_data.get('six_digit_number')
        if not value.isdigit():
            raise ValidationError('This field must contain only digits.')
        
        return value


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('User with this email does not exists')
        
        return email


class CustomPasswordResetFormDone(forms.Form):
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        help_text=""
    )
    retype_password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=100,
        help_text=""
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')

        if password and retype_password and password != retype_password:
            raise ValidationError("Passwords do not match.")
        
        if retype_password and len(retype_password) < 8:
            raise ValidationError('Password must be at least 8 characters.')
                        
        return password


class LoginForm(AuthenticationForm):
    recaptcha = ReCaptchaField(
        error_messages={
            'required': 'reCAPTCHA verification is required to continue.',
            'invalid': 'The reCAPTCHA response is invalid. Please try again.',
        }
    )


class ProfileFormCustomer(ModelForm):
    email = forms.EmailField(max_length=254, required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
        })
    )
    username = forms.CharField(max_length=154, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.get(email=self.user.email)

        if User.objects.filter(email=email).exclude(email=user.email).exists():
            raise ValidationError("Email already taken")
        else:
            return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        user = User.objects.get(username=self.user.username)

        if User.objects.filter(username=username).exclude(username=user.username).exists():
            raise ValidationError("username already taken")
        else:
            return username

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('user', 'avatar',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class CustomerForm(ModelForm):
    email = forms.EmailField(max_length=254, required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
        })
    )
    username = forms.CharField(max_length=154, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
        })
    )
    password1 = forms.CharField(max_length=120, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password1',
        })
    )
    password2 = forms.CharField(max_length=120, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password2',
        })
    )
    recaptcha = ReCaptchaField(
        error_messages={
            'required': 'reCAPTCHA verification is required to continue.',
            'invalid': 'The reCAPTCHA response is invalid. Please try again.',
        }
    )

    class Meta:
        model = Customer
        exclude = ('user', 'avatar', 'meddle_name',)
    

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        if password2 and len(password2) < 8:
            raise ValidationError('Password must be at least 8 characters.')
                        
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already taken")
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken")
        
        return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number and not re.match(r'^\+?\d{7,15}$', phone_number):
            raise ValidationError('Enter a valid phone number.')

        if phone_number and Customer.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This phone number is already in use.')

        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                if field.label is None:
                    field.label = field_name.capitalize()
                field.label = f"{field.label} * "
