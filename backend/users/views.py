from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from djoser import serializers as djoser_serializers
from djoser.permissions import CurrentUserOrAdmin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow
from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post')

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'set_password':
            return djoser_serializers.SetPasswordSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            self.permission_classes = [AllowAny]
        elif self.action == 'set_password':
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def get_instance(self):
        return self.request.user

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_200_OK)


class SubscriptionsListViewSet(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        follow_objects = get_list_or_404(Follow, user=self.request.user)
        subscriptions = [object_.following for object_ in follow_objects]
        return subscriptions


class SubscribeViewSet(APIView):

    def get(self, request, id):
        if request.user == get_object_or_404(User, id=id):
            return Response(
                {'errors': 'Unable to subscribe to yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        following = get_object_or_404(User, id=id)
        follow_object = Follow.objects.filter(
            user=request.user,
            following=following
        )

        if not follow_object:
            Follow.objects.create(
                user=request.user,
                following=following
            )
            serializer = UserSerializer(
                following,
                context={'request': self.request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'You are already subscribed to the user'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        following = get_object_or_404(User, id=id)
        follow_object = Follow.objects.filter(
            user=request.user,
            following=following
        )
        if follow_object:
            follow_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'You are not subscribed to the user'},
            status=status.HTTP_400_BAD_REQUEST
        )
