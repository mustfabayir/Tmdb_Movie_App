from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

TMDB_API_KEY = '32abbbb5a957b4da049ca3b862bba021'

# Create your views here.

class IndexTemplateView(TemplateView):
    index_key = {
        'now-playing': 'movie/now_playing', # index
        'popular': 'movie/popular', 
        'top-rated': 'movie/top_rated',
        'trending': 'movie/trending',
        'upcoming': 'movie/upcoming',
        'tv-popular': 'tv/popular',
        'tv-on-the-air': 'tv/on_the_air',
        'tv-top-rated': 'tv/top_rated',
        }
    template_name = "my_app/index.html"
    def get_context_data(self, trend='now-playing', **kwargs):
        
        # print(self.request.__dict__)
        # print(self['password'])
        # print(kwargs)
        data = []
        for i in range(1, 2):
            i += 1
            name = f"https://api.themoviedb.org/3/{self.index_key[trend]}?api_key={TMDB_API_KEY}&language=en-US&page={i}"
            f_data = requests.get(name).json()['results']
            data.extend(f_data)
        paginator = Paginator(data, 20)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return context


def search(request):
    data = []
    query = request.GET.get('q')
    
    if query:
        name = f"https://api.themoviedb.org/3/search/tv?query={query}&api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false"
        f_data = requests.get(name).json()['results']
        data.extend(f_data)
    else:
        return HttpResponse("Please enter a search query")

    paginator = Paginator(data, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'my_app/result.html', context)