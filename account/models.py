from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountManager(BaseUserManager):
    def craete_user(self, email, username, password=None):
        if not email:
            raise ValueError('ایمیل صحیح وارد کنید.')
        if not username:
            raise ValueError('نام کاربری اشتباه است.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.is_active = True

        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.craete_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


def get_imag_profile(self, filename):
    return f'profile_image/{self.pk}/{filename}'


def get_default_profile():
    return 'img/user.png'


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='ایمیل', max_length=60, unique=True)
    username = models.CharField(
        max_length=35, unique=True, verbose_name='نام کاربری')
    date_joined = models.DateTimeField(auto_now=True, verbose_name='زمان ثبت نام')
    last_login = models.DateTimeField(auto_now_add=True, verbose_name='زمان خروج')
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_superuser= models.BooleanField(default=False, verbose_name='مدیر اصلی')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_staff = models.BooleanField(default=False, verbose_name='  کارمند')
    profile_image = models.ImageField(upload_to='user_profile', null=True, blank=True)
    hide_email = models.BooleanField(default=False, verbose_name='ایمیل نمایش داده شود ؟ ')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    object = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_image/' + str(self.pk) + "/")]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.is_admin




