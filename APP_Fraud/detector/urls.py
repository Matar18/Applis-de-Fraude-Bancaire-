from django.urls import path
from . import views


app_name = 'detector'

urlpatterns = [
    path('', views.predict_view, name='predict'),
    path('historique/', views.history_views, name="history"),
    path('dashboard/', views.dashboard, name="dashboard")
]