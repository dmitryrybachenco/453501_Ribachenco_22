from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('category/<int:pk>/', views.service_category_detail, name='category_detail'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
]