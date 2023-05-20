from django.shortcuts import render
from django.views import View


# Create your views here.


class Home(View):
    templates_name = 'home/index.html'

    def get(self, request):
        return render(request, self.templates_name, {})
