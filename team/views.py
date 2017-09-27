from django.shortcuts import render
from django.views import View


# Create your views here.
class Team(View):
    '''
    team view
    '''
    def get(self, request):
        '''
        the team page
        :param request: request object
        :return: team page
        '''
        return render(request, 'team/team.html', context={'url': 'team'})
