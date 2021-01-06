import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db import models


class Freebie(models.Model):
    """
    Base model that includes default created / updated timestamps.
    """
    ip = models.GenericIPAddressField() 
    counter = models.IntegerField(default=0)
