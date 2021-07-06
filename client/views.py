from rest_framework import status, generics, filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Client, Worker, User, RequestedService, WorkerPortfolio, WorkerPortfolioPhoto, RequestPhoto, Response as Resp
from .serializers import LoginSerializer, ClientRegistrationSerializer, \
    WorkerRegistrationSerializer, UserSerializer, WorkerSerializer, PortfolioSerializer, ServiceSerializer, \
    WorkerPhotoSerializer, PhotoSerializer, ResponseSerializer, ResponseRegSerializer


class ClientRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ClientRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class WorkerRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = WorkerRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class ResponseRegAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResponseRegSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Response created  successfully',
        }

        return Response(response)


class ResponseConfirmAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # worker = Worker.objects.get(id=request.worker_id)
        service = RequestedService.objects.filter(id=request.data['request_id']).update(worker=request.data['worker_id'], status=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Response confirmed  successfully',
        }
        return Response(response)



class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class ClientProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer
    def get(self, request):
        try:
            user_profile = Client.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.user.first_name,
                    'last_name': user_profile.user.last_name,
                    'email': user_profile.user.email,
                }]
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class WorkerProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user_profile = Worker.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            worker_p = user_profile.get_worker_portfolio()
            list = []
            for i in range(len(worker_p)):
                list.append(PortfolioSerializer(worker_p[i]).data)
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.user.first_name,
                    'last_name': user_profile.user.last_name,
                    'email': user_profile.user.email,
                    'portfolios': list
                }]
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class RequestListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        id = self.request.query_params.get('user_id')
        if id is not None:
            return RequestedService.objects.filter(client=id)
        else:
            return RequestedService.objects.all()


class RequestListDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = RequestedService.objects.all()
    serializer_class = ServiceSerializer


class RequestPhotoSerializerAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        id = self.request.query_params.get('request_id')
        if id is not None:
            return RequestPhoto.objects.filter(request=id)
        else:
            return RequestPhoto.objects.all()

class RequestPhotoSerializerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = RequestPhoto.objects.all()
    serializer_class = PhotoSerializer


class UserListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(is_client=True)
    serializer_class = UserSerializer


class WorkerListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$categories__title']


class WorkerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(is_worker=True)
    serializer_class = UserSerializer


class ClientDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(is_client=True)
    serializer_class = UserSerializer


class WorkerPortfolioPhotoAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = WorkerPhotoSerializer

    def get_queryset(self):
        id = self.request.query_params.get('portfolio_id')
        if id is not None:
            return WorkerPortfolioPhoto.objects.filter(workerPortfolio=id)
        else:
            return WorkerPortfolioPhoto.objects.all()


class WorkerPortfolioPhotoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = WorkerPortfolioPhoto.objects.all()
    serializer_class = WorkerPhotoSerializer


class WorkerPortfolioAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        id = self.request.query_params.get('user_id')
        if id is not None:
            return WorkerPortfolio.objects.filter(worker=id)
        else:
            return WorkerPortfolio.objects.all()


class WorkerPortfolioDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = WorkerPortfolio.objects.all()
    serializer_class = PortfolioSerializer


class ResponseListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResponseSerializer

    def get_queryset(self):
        worker_id = self.request.query_params.get('worker_id')
        request_id = self.request.query_params.get('request_id')
        if worker_id is not None:
            return Resp.objects.filter(worker=worker_id)
        elif request_id is not None:
            return Resp.objects.filter(request=request_id)
        else:
            return Resp.objects.all()


class ResponseListDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Resp.objects.all()
    serializer_class = ResponseSerializer
