from django.urls import path
from movie_app import views
from . import swagger

urlpatterns = [
    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('movies/', views.MovieListAPIView.as_view()),
    path('movies/<int:id>/', views.MovieDetailAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('movies/<int:id>/reviews/', views.movie_review_list_api_view),
]

urlpatterns += swagger.urlpatterns
