from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('analysis/', views.content_analysis, name='analysis'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/kpis/', views.api_kpis, name='api_kpis'),
]
