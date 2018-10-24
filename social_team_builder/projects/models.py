from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db import models


class Project(models.Model):
    user = models.ForeignKey(User, related_name="project")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    timeline = models.IntegerField()
    requirements = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={'pk': self.pk})


class Position(models.Model):
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

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    skill = models.CharField(max_length=20, choices=SKILLES_CHOICES, default="")
    
    def __str__(self):
        return self.title

    """
    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={'pk':self.pk})
    """
