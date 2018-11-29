from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import User
from . models import Project, Position, Application, Notification
from .forms import ProjectForm, PositionForm


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="yasuko",
            email="test@gmail.com",
            password="testpassword"
        )
        self.client.login(username="yasuko", email="test@gmail.com", password="testpassword")


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="yasuko",
            email="test@gmail.com",
            password="testpassword"
        )

        self.user_2 = User.objects.create_user(
            username="user_2",
            email="test@test.com",
            password="testpassword"
        )

        self.test_project = Project.objects.create(
            user=self.user,
            title="test project",
            description="test",
            estimated_time=1,
            requirements="something"
        )

        self.test_position = Position.objects.create(
            project=self.test_project,
            title="test position",
            description="test",
            skill="Python",
        )

        self.test_application = Application.objects.create(
            applicant=self.user_2,
            position=self.test_position,
            status="new",
        )

        self.test_notification = Notification.objects.create(
            user=self.user,
            application=self.test_application,
            message="Your application is approved!"
        )


    def test_project_list_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')
        self.assertContains(resp, self.test_project.title)


    def test_project_create(self):
        # only logged in user allows access to create entry
        resp = self.client.get(reverse('projects:create'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(email="test@gmail.com", password="testpassword")
        resp = self.client.get(reverse('projects:create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_form.html')


    def test_project_detail_view(self):
        self.client.login(email="test@gmail.com", password="testpassword")
        resp = self.client.get(reverse('projects:project_detail',
                                kwargs={'pk': self.test_project.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_project, resp.context['project'])
        self.assertTemplateUsed(resp, 'projects/project_detail.html')


    def test_application_list(self):
        self.client.login(email="test@gmail.com", password="testpassword")
        resp = self.client.get(reverse('projects:application'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/application_list.html')


    def test_notification_list(self):
        self.client.login(email="test@gmail.com", password="testpassword")
        resp = self.client.get(reverse('projects:notification'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/notification.html')
