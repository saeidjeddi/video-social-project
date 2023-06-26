from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from account.forms import RegisteriosnForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core import files



# Create your views here.


class RegisterView(View):
    form_class = RegisteriosnForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):


        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Account.object.craete_user(email=cd.get('email').lower(), username=cd.get('username'),password=cd.get('password1'))
            login(request, user)

            return redirect('home:index')
        return render(request, self.template_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home:index")


class LoginView(View):
    form_class = AccountAuthenticationForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)

                return redirect('home:index')

        return render(request, self.template_name, {'form': form})


class EditProfilerView(LoginRequiredMixin, View):
    form_class = AccountUpdateForm

    def get(self, request, *args, **kwrags):
        user_id = kwrags.get('user_id')
        form = self.form_class = AccountUpdateForm(instance=request.user)
        return render(request, "account/etit_profil.html", {'form': form})

    def post(self, request, *args, **kwrags):
        dic = {}
        user_id = kwrags.get('user_id')
        account = Account.object.get(pk=user_id)
        form = self.form_class = AccountUpdateForm(request.POST, request.FILES, instance=request.user,
                                                   initial={'email': account.email,
                                                            'username': account.username,
                                                            'profile_image': account.profile_image,
                                                            'hide_email': account.hide_email})
        if form.is_valid():
            form.save()
            return redirect('home:index')



        dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

        return render(request, "account/etit_profil.html",)
