from rest_framework import viewsets, filters, permissions, serializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .mixins import CategoryGenreModelMixin
from .filters import TitleFilter
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, CommentSerializer,
    ReviewSerializer, TitleCreateSerializer
)
from .permissions import (
    IsAdministratorOrReadOnly, IsAuthorAdminModeratorOrReadOnly
)
from reviews.models import Category, Genre, Title, Review


class CategoryViewSet(CategoryGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdministratorOrReadOnly]
    lookup_field = 'slug'


class GenreViewSet(CategoryGenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdministratorOrReadOnly]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    rating = serializers.IntegerField(read_only=True)
    serializer_class = TitleSerializer
    permission_classes = [IsAdministratorOrReadOnly]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly, permissions.IsAuthenticatedOrReadOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('author', 'text', 'review', )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('author', 'text', 'title',)

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)
