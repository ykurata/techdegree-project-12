from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


ANDROID = "Android"
DESIGN = "Design"
JAVA = "Java"
PHP = "PHP"
PYTHON = "Python"
RAILS = "Rails"
WORDPRESS = "Wordpress"
iOS = "iOS"
SKILLES_CHOICES = (
    (ANDROID, "Android Developer"),
    (DESIGN, "Designer"),
    (JAVA, "Java Developer"),
    (PHP, "PHP Developer"),
    (PYTHON, "Python Developer"),
    (RAILS, "Rails Developer"),
    (WORDPRESS, "Wordpress Developer"),
    (iOS, "iOS Developer")
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    bio = models.CharField(max_length=255, blank=True, default="")
    image = models.ImageField(upload_to="profile_image/", blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username


ANDROID = "Android"
DESIGN = "Design"
JAVA = "Java"
PHP = "PHP"
PYTHON = "Python"
RAILS = "Rails"
WORDPRESS = "Wordpress"
iOS = "iOS"
SKILLES_CHOICES = (
    (ANDROID, "Android"),
    (DESIGN, "Design"),
    (JAVA, "Java"),
    (PHP, "PHP"),
    (PYTHON, "Python"),
    (RAILS, "Rails"),
    (WORDPRESS, "Wordpress"),
    (iOS, "iOS")
)

class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    name = models.CharField(max_length=20, choices=SKILLES_CHOICES)

    def __str__(self):
        return self.name
