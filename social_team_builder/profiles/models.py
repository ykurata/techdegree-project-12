from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    skill = models.CharField(max_length=25, choices=SKILLES_CHOICES)

    def __str__(self):
        return self.user
