from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')


urlpatterns = [
    path(
        'subscriptions/',
        views.SubscriptionsListViewSet.as_view(),
        name='subscriptions'),
    path(
        '<int:id>/subscribe/',
        views.SubscribeViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls))
]
