from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('get-results', views.GetResultsView.as_view(), name='search_result')
]