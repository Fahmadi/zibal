from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import *


class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    user_pic = models.FileField(upload_to='zibal/gateway/pic_folder/',null = True, validators=[validate_file_extension] )


