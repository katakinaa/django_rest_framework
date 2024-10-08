from django.db.models import Avg
from rest_framework import serializers
from movie_app.models import Director, Movie, Review


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
