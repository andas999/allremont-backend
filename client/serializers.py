from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import User, Client, Worker, RequestedService, RequestPhoto, Response, WorkerPrice
from rest_framework_jwt.settings import api_settings

from .models import Categories, WorkerPortfolio, WorkerPortfolioPhoto

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class ClientRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'token']

    def create(self, validated_data):
        user = User.objects.create_client(**validated_data)
        Client.objects.create_user(user)
        return user


class WorkerRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'token', ]

    def create(self, validated_data):
        user = User.objects.create_worker(**validated_data)
        Worker.objects.create_user(user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'date_joined', 'is_client', 'is_worker', 'email', 'SMSVerification']


class UserRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['title']


class WorkerSerializer(serializers.ModelSerializer):
    worker_price = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Worker
        fields = '__all__'

    def get_worker_price(self, obj):
        ser = WorkerPriceSerializer
        return ser(obj.worker_price, many=True).data

class WorkerRespSerializer(serializers.ModelSerializer):
    user = UserRespSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'user']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerPortfolio
        fields = '__all__'


class WorkerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerPortfolioPhoto
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestPhoto
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedService
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    class Meta:
        model = Response
        fields = '__all__'

    def get_worker(self, obj):
        u = Worker.objects.get(user=obj.worker.user)
        return WorkerRespSerializer(u).data


class ResponseRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


class WorkerPriceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = WorkerPrice
        fields = '__all__'


class WorkerPriceCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerPrice
        fields = '__all__'