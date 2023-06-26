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



class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'profile_image', 'hide_email')

        widgets = {
            "email": forms.TextInput(attrs={
                'class': "form-control rounded-0",
                "placeholder": 'ایمیل'
            }),
            "username": forms.TextInput(attrs={
                'class': "form-control rounded-0",
                "placeholder": 'نام کاربری'
            }),
            # "profile_image": forms.TextInput(attrs={
            #     'class': "form-control form-control-sm",
            #     'id': "formFileMultiple",
            #     'type': "file",
            # }),

        }
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.object.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("ایمیل '%s' تکراری هست " % email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.object.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError("نام کاربری '%s' تکراری هست " % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account

