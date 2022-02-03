from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        user = self.create_user(
            email,
            nickname = nickname
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)

    is_staff = models.BooleanField(default=False)
    created_time = models.DateTimeField(default = timezone.now)
    updated_time = models.DateTimeField(default = timezone.now)

    object = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    class Meta:
        db_table = 'User'


class Sneakers(models.Model):
    sneaker_name = models.CharField(max_length=200)
    sneaker_name_ko = models.CharField(max_length=200,default='')
    model_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    total_count = models.IntegerField(default=0)
    cop_count = models.IntegerField(default=0)
    cop_percent = models.FloatField(default=0)
    thumbnail = models.ImageField(upload_to = '', blank = True)
    retail_date = models.DateField()
    created_time = models.DateTimeField(default = timezone.now)
    updated_time = models.DateTimeField(default = timezone.now)
    views = models.PositiveIntegerField(default=0,verbose_name='조회수') # 음수제거

    def __str__(self):
        return self.model_number

    @property
    def update_view_count(self):
        self.views = self.views + 1
        self.save()

    class Meta:
        db_table = 'sneakers'


class Comment(models.Model):
    board_id  = models.ForeignKey(Sneakers, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    created_time = models.DateTimeField(default = timezone.now)
    updated_time = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = 'comments'

class CopOrDrop(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.PROTECT)
    board_id  = models.ForeignKey(Sneakers, on_delete=models.CASCADE)
    choice = models.BooleanField()

    class Meta:
        db_table = 'CopTable'

class ScoreBoard(models.Model):
    board_id  = models.ForeignKey(Sneakers, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    score = models.FloatField()
    created_time = models.DateTimeField(default = timezone.now)
    updated_time = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = 'sneakers_score'
    

class Keyword(models.Model):
    keyword = models.CharField(max_length=30)
    sneaker_id = models.ForeignKey(Sneakers,on_delete=models.CASCADE)

    class Meta:
        db_table = 'keyword'


    def __str__(self):
        return self.keyword


class UserMovementOfViews(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    sneaker_id = models.ForeignKey(Sneakers,on_delete=models.CASCADE)
    movement_time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'user_movements_of_views'

class SearchRequest(models.Model):
    keyword = models.CharField(max_length=200)
    request_time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'requests_of_search'

