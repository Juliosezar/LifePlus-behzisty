from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # We don't need to add anything here. 
    # AbstractUser already enforces Username and Password login.
    pass
