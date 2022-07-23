from rest_framework import routers
from django.urls import include, path

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet
)
from users.views import APIGetToken, APISignup, UsersViewSet

router = routers.DefaultRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
