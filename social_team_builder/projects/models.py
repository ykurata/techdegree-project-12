from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

from django.db import models


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    estimated_time = models.IntegerField()
    requirements = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={
                        'pk': self.pk})
    

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

    project = models.ForeignKey(
        Project,
        null=True,
        related_name="positions",
        on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    skill = models.CharField(
        max_length=20,
        choices=SKILLES_CHOICES,
        default="",
        blank=True)
    position_filled = models.BooleanField(default=False, blank=True)
    applicants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Application')

    def __str__(self):
        return self.title


class Application(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="applicaion",
        on_delete=models.DO_NOTHING
    )
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20)

    def __str__(self):
        return "{}, {}".format(self.applicant, self.position)


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notification",
        on_delete=models.DO_NOTHING
    )
    application = models.ForeignKey(Application, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)
