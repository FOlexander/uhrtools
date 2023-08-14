from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CheckboxInput


# Create your models here.
class CustomUser(AbstractUser):
    # Add additional fields here
    term_of_use_privasy_ploicy = models.BooleanField(null=True)
