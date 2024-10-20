from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import (DirectorSerializer, MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer,
                                   DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer)
from rest_framework import status


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def director_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.annotate(movies_count=Count('movie'))
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        name = serializer.validated_data.get('name')

        director = Director.objects.create(
            name=name
        )
        director.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'director_id': director.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(instance=director, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        data = MovieSerializer(instance=movie, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')

        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Director not found"})

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director=director
        )
        movie.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'movie_id': movie.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(instance=movie, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_list_create_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(instance=review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie_id')

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Movie not found"})

        review = Review.objects.create(
            text=text,
            stars=stars,
            movie=movie
        )
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'review_id': review.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance=review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.save()
        return Response(data=ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movies = Movie.objects.all()
    data = MovieWithReviewsSerializer(instance=movies, many=True).data
    return Response(data=data)
