from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db import models

from markdown_deux import markdown


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
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
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    skill = models.CharField(max_length=20, choices=SKILLES_CHOICES, default="")
    position_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Application(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="applicaion"
    )
    position = models.ForeignKey(Position)
    status = models.CharField(max_length=20)

    def __str__(self):
        return "{}, {}".format(self.applicant, self.position)


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notification"
    )
    application = models.ForeignKey(Application)
    message = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)
