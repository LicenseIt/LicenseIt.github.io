import requests
import json
import time
import logging
from itertools import chain

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Search, Track, Collection, Artist


class SearchView(View):
    '''
    The search view
    '''
    template_name = 'search/results.html'

    def get(self, request, *args, **kwargs):
        '''
        Return the search page
        :param request: the request object
        :return:
        '''
        return render(request, self.template_name, context={'url': 'search'})

    def post(self, request, *args, **kwargs):
        '''
        The actual search to be done.

        We save the data we get back from itunes to our db and then redirect
        back to results, which have all the results of the search from itunes
        :param request: the request object
        :return:
        '''
        logger = logging.getLogger(__name__)
        search = request.POST['search']
        search_in_db = Search.objects.filter(search_term=search)
        print(search_in_db)
        if search_in_db.exists():
            return HttpResponseRedirect(reverse('results_page', args=(search_in_db[0].id,)))
        search_db = Search()
        search_db.search_term = search
        search_db.save()
        res = requests.get('https://itunes.apple.com/search',
                           params={'term': search})

        ret = json.loads(res.text)
        results = ret['results']

        for result in results:
            logger.info(result)
            artist = Artist()
            artist.name = result['artistName']
            artist.save()
            collection = Collection()

            if 'collectionName' in result:
                collection.name = result['collectionName']
            else:
                collection.name = ''

            collection.artist = artist
            collection.save()
            track = Track()

            if 'trackName' in result:
                track.name = result['trackName']
            else:
                track.name = ''

            track.collection = collection
            track.artist = artist

            if 'kind' in result:
                track.kind = result['kind']
            else:
                track.kind = ''

            if 'trackTimeMillis' in result:
                track.track_time = result['trackTimeMillis']
            else:
                track.track_time = 0

            if 'artworkUrl100' in result:
                track.artwork_100 = result['artworkUrl100']
            else:
                track.artwork_100 = ''

            if 'artworkUrl60' in result:
                track.artwork_60 = result['artworkUrl60']
            else:
                track.artwork_60 = ''

            if 'description' in result:
                track.description = result['description']

            if 'primaryGenreName' in result:
                track.genre_category = result['primaryGenreName']

            if 'releaseDate' in result:
                date = time.strptime(result['releaseDate'], '%Y-%m-%dT%H:%M:%SZ')
                track.release_date = time.strftime('%Y-%m-%d', date)

            if 'copyright' in result:
                track.media_copyright = result['copyright']

            track.search = search_db
            track.save()

        return HttpResponseRedirect(reverse('results_page', args=(search_db.id,)))


class ResultsView(View):
    template_name = 'search/results.html'
    results_per_page = 10

    def get(self, request, pk, *args, **kwargs):
        results = Track.objects.filter(search=pk)
        results_count = len(results)
        if results_count < 11:
            results = list(chain(results, Track.objects.all()[:10]))
        paginator = Paginator(results, self.results_per_page)
        page = request.GET.get('page')
        is_first = True
        try:
            page_results = paginator.page(page)
            is_first = False
        except PageNotAnInteger:
            page_results = paginator.page(1)
        except EmptyPage:
            page_results = paginator.page(paginator.num_pages)
        current_page = page_results.number
        prev_prev = current_page - 2 if current_page > 2 else None
        prev = current_page - 1 if page_results.has_previous() else None
        next_next = current_page + 2 if current_page + 2 <= paginator.num_pages else None
        _next = current_page + 1 if page_results.has_next() else None
        context = {
            'results': page_results,
            'num_of_results': len(results),
            'prev_prev': prev_prev,
            'prev': prev,
            'current': current_page,
            'next': _next,
            'next_next': next_next,
            'url': 'results',
            'num_pages': paginator.num_pages
        }

        if is_first:
            context['first'] = True

        return render(request, self.template_name, context=context)
