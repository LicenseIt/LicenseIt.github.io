import requests
import json
import time
import logging

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Search, Track, Collection, Artist


class SearchView(View):
    '''
    The search page
    '''
    def get(self, request, *args, **kwargs):
        '''
        Return the search page
        :param request:
        :return:
        '''
        return render(request, 'search/search.html')

    def post(self, request, *args, **kwargs):
        '''
        The actual search to be done.

        We save the data we get back from itunes to our db and then redirect
        back to results, which have all the results of the search from itunes
        :param request:
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
    def get(self, request, pk, *args, **kwargs):
        results = Track.objects.filter(search=pk)
        paginator = Paginator(results, 10)
        page = request.GET.get('page')
        try:
            page_results = paginator.page(page)
        except PageNotAnInteger:
            page_results = paginator.page(1)
        except EmptyPage:
            page_results = paginator.page(paginator.num_pages)
        context = {'results': page_results, 'num_of_results': results.count()}
        return render(request, 'search/results.html', context=context)
