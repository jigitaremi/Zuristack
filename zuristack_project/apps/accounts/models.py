from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

from .managers import CustomUserManager
from . import utils
# Create your models here.

class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)

    slug = models.SlugField(blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta: 
        ordering = ["email"]
        verbose_name = "User"

    def __str__(self):
        return self.email
    
    #Creating a defualt slug/username for users if blank 

    
    def gen_random_slug(self):
        random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id())
        while CustomUser.objects.filter(slug=random_slug).exists():
            random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id())
        return random_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.gen_random_slug()
    
        super().save(*args, **kwargs)