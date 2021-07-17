from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('worker/add/', WorkerRegistrationAPIView.as_view(), name='worker_registration'),
    path('client/add/', ClientRegistrationAPIView.as_view(), name='client_registration'),
    re_path(r'^worker/profile', WorkerProfileView.as_view()),
    re_path(r'^client/profile', ClientProfileView.as_view()),
    path('users/', UserListAPI.as_view()),
    path('users/<int:pk>/', UserDetailAPI.as_view()),
    path('users/clients', ClientListAPI.as_view()),
    path('users/clients/<int:pk>/', ClientDetailAPI.as_view()),
    path('users/workers', WorkerListAPI.as_view()),
    path('users/workers/categories', WorkerCatListAPI.as_view()),
    path('users/workers/<int:pk>/', WorkerDetailAPI.as_view()),
    path('requests/', RequestListAPI.as_view()),
    path('requests/<int:pk>/', RequestListDetailAPI.as_view()),
    path('requests/avgcost', RequestAverageCostAPI.as_view()),
    path('requests/photo/', RequestPhotoSerializerAPI.as_view()),
    path('requests/photo/<int:pk>', RequestPhotoSerializerDetailAPI.as_view()),
    path('responses/', ResponseListAPI.as_view()),
    path('responses/<int:pk>/', ResponseListDetailAPI.as_view()),
    path('responses/add/', ResponseRegAPIView.as_view()),
    path('responses/confirm/', ResponseConfirmAPI.as_view()),
    path('users/workers/portfolios/', WorkerPortfolioAPI.as_view()),
    path('users/workers/portfolio/<int:pk>/', WorkerPortfolioDetailAPI.as_view()),
    path('users/workers/portfolio/photo/', WorkerPortfolioPhotoAPI.as_view()),
    path('users/workers/portfolio/photo/<int:pk>', WorkerPortfolioPhotoDetailAPI.as_view())
]
