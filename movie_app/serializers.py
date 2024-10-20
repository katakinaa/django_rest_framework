from django.db.models import Avg
from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieWithReviewsSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'director', 'reviews', 'rating']

    def get_reviews(self, movie):
        reviews = Review.objects.filter(movie=movie)
        return [{'text': review.text, 'stars': review.stars} for review in reviews]

    def get_rating(self, movie):
        rating = Review.objects.filter(movie=movie).aggregate(Avg('stars')).get('stars__avg')
        return round(rating, 2) if rating else None


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def validate(self, attrs):
        director_id = attrs.get('id')
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return attrs


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    duration = serializers.CharField()
    director = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        movie_id = attrs.get('id')
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie does not exist!')
        return attrs


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(min_value=1)
    movie = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        review_id = attrs.get('id')
        try:
            Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise ValidationError('Review does not exist!')
        return attrs
