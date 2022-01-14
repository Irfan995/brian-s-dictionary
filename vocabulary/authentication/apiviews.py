from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status 
from rest_framework.permissions import IsAuthenticated
from authentication.serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from django.http import Http404


class UserRegistrationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # if user:
        #     UserInformation.objects.create(
        #         user=user
        #     )

        data = serializer.data

        return Response(data, status=status.HTTP_201_CREATED)


class UsernameAPIView(APIView):
    permission_classes = []

    def get(self, request):
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
            
            data = {
                'username': user.username
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            user = User.objects.get(email=username)
            
            data = {
                'username': user.username
            }

            return Response(data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegistrationSerializer

    def get_object(self):
        try:
            return self.request.user
        except:
            Http404

    def get(self, request):
        user = self.get_object()
        print(user)
        serializer = UserRegistrationSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)