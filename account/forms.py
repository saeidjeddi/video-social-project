from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate


class RegisteriosnForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='ایمیل وارد کنید')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.object.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("ایمیل '%s' تکراری هست " % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.object.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError("نام کاربری '%s' تکراری هست " % account)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('ورود ناموفق ')

