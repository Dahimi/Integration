from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Home/', views.Home, name='home'),
    path('Problem/<int:id>/lunch_tests/', views.Lunch_Tests),
    path('', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('Problem/<int:id>/', views.Solve_Problem, name='problem'),
    path('Ranking/', views.Ranking, name='ranking'),
]