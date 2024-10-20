from django.urls import path
from movie_app import views

urlpatterns = [
    path('', views.director_list_create_api_view),
    path('<int:id>/', views.director_detail_api_view),
    path('', views.movie_list_create_api_view),
    path('<int:id>/', views.movie_detail_api_view),
    path('', views.review_list_create_api_view),
    path('<int:id>/', views.review_detail_api_view),
    path('', views.movie_review_list_api_view),
]
