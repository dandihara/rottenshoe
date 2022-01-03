from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.deletion import CASCADE
from django.conf import settings

# user(Ab) / board / like / comment
# Create your models here.


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


class SneakerBoard(models.Model):
    sneaker_name = models.CharField(max_length=200)
    model_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    hot_score = models.FloatField(default=0.0)
    thumbnail = models.ImageField(upload_to = settings.MEDIA_ROOT, blank = True)
    retail_date = models.DateField()

    def __str__(self):
        return self.model_number


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)

    is_staff = models.BooleanField(default=False)

    object = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

class Comment(models.Model):
    board_id  = models.ForeignKey(SneakerBoard, on_delete=CASCADE)
    user_id = models.ForeignKey(User, on_delete = CASCADE)
    comment = models.TextField()

class ScoreBoard(models.Model):
    board_id  = models.ForeignKey(SneakerBoard, on_delete=CASCADE)
    user_id = models.ForeignKey(User, on_delete = CASCADE)
    score = models.FloatField()
    

