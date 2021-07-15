from rest_framework import serializers
from .models import User, Client, Worker, RequestedService, RequestPhoto, Response, WorkerPrice

from .models import Categories, WorkerPortfolio, WorkerPortfolioPhoto


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'date_joined', 'is_client', 'is_worker', 'email',]


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
