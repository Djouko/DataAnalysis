from django.urls import path
from . import views

urlpatterns = [
    path('values/', views.anova_view, name='anova_values'),
    path('index', views.index, name='index'),
    path('', views.home, name='home'),
    path('data/', views.validate_params, name='validate_params'),
]