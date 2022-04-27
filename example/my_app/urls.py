from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='base'),
    path('index/<trend>', views.IndexTemplateView.as_view(), name='index'),
    path("search/", views.search, name="search"),

]
