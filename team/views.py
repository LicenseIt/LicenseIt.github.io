from django.shortcuts import render
from django.views import View


# Create your views here.
class Team(View):
    def get(self, request):
        return render(request, 'team/team.html', context={'url': 'team'})
