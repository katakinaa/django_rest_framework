from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer
from rest_framework import status


@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    directors = Director.objects.annotate(movies_count=Count('movie'))
    data = DirectorSerializer(instance=directors, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(instance=director, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movie = Movie.objects.all()
    data = MovieSerializer(instance=movie, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(instance=movie, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    data = ReviewSerializer(instance=review, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(instance=review, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movies = Movie.objects.all()
    data = MovieWithReviewsSerializer(instance=movies, many=True).data
    return Response(data=data)
