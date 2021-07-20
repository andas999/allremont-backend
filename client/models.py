import jwt
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.conf import settings


def upload_works(instance, filename):
    return filename


def upload_schemas(instance, filename):
    return filename


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The specified username must be set')

        if not email:
            raise ValueError('This email address must be set')

        if not password:
            raise ValueError('This password must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)

    def create_worker(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_worker', True)

        if extra_fields.get('is_worker') is not True:
            raise ValueError('Worker must have is_worker = True')

        return self._create_user(username, email, password, **extra_fields)

    def create_client(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_client', True)

        if extra_fields.get('is_client') is not True:
            raise ValueError('Client must have is_client = True')

        return self._create_user(username, email, password, **extra_fields)


class ClientManager(BaseUserManager):

    def _create_user(self, user=None):
        client = self.model(user=user)
        client.save(using=self.db)
        return client

    def create_user(self, user=None):
        return self._create_user(user)


class WorkerManager(BaseUserManager):
    def _create_user(self, user=None):
        worker = self.model(user=user)
        worker.save(using=self._db)
        return worker

    def create_user(self, user=None):
        return self._create_user(user)


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=False)
    user.is_client = True

    objects = ClientManager()

    def __str__(self):
        return self.user.username

    def has_module_perms(self, app_label):
        return self.user.is_superuser

    def has_perm(self, perm, obj=None):
        return self.user.is_superuser


class WorkerPrice(models.Model):
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_price')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Price', null=False, default=0)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=False)
    # categories = models.ManyToManyField('Categories', null=True)
    response_num = models.IntegerField(null=True)
    objects = WorkerManager()

    def __str__(self):
        return self.user.username

    def has_module_perms(self, app_label):
        return self.user.is_superuser

    def has_perm(self, perm, obj=None):
        return self.user.is_superuser

    # def get_categories(self):
    #     return Categories.objects.filter(worker=self)

    def get_worker_portfolio(self):
        return WorkerPortfolio.objects.filter(worker=self)


class WorkerPortfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Name of the work", max_length=500, null=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def get_photos(self):
        return WorkerPortfolioPhoto.objects.filter(workerPortfolio=self)


class WorkerPortfolioPhoto(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=20, null=False, default='default')
    image_url = models.ImageField(_("Image"), upload_to=upload_works, default='default.jpg')
    workerPortfolio = models.ForeignKey(WorkerPortfolio, on_delete=models.CASCADE, null=True)


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Title", max_length=255, null=False)
    description = models.CharField(verbose_name="Description", max_length=255, null=False)
    created_on = models.DateTimeField(verbose_name="Created on", auto_now_add=True)

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Title", max_length=255, null=False)
    description = models.CharField(verbose_name="Description", max_length=255, null=False)
    created_on = models.DateTimeField(verbose_name="Created on", auto_now_add=True)

    def __str__(self):
        return self.title


class RequestedService(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, default='')
    sub_category = models.ForeignKey('SubCategories', on_delete=models.CASCADE, default='')
    workload = models.IntegerField(verbose_name='Workload', null=False, default=0)
    timing = models.IntegerField(verbose_name='Number of days', null=False, default=0)
    address = models.CharField(verbose_name='Address', null=False, max_length=255, default='')
    budget = models.IntegerField(verbose_name='Budget', null=False, default=0)
    created_on = models.DateTimeField(verbose_name="Created on", default=timezone.now())
    status = models.BooleanField(verbose_name="Status", default=False)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.address


class RequestPhoto(models.Model):
    image_name = models.CharField(max_length=20, null=False, default='default')
    image_url = models.ImageField(_("Image"), upload_to=upload_schemas, default='default2.jpg')
    request = models.ForeignKey(RequestedService, on_delete=models.CASCADE, null=True)


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey('RequestedService', on_delete=models.CASCADE)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    response_detail = models.CharField(verbose_name='Details', max_length=300)


class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name='client')
    comment = models.TextField(null=True, verbose_name='comment')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='worker')
    rate = models.IntegerField(verbose_name='rate')

    def __str__(self):
        return self.comment