from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),
    path('<user_id>/edit', views.EditProfilerView.as_view(), name='edit'),

]
