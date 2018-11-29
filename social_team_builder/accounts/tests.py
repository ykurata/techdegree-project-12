from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import User, Skill
from .forms import UserCreateForm, ProfileForm, SkillForm


class UserModelTest(TestCase):
    def test_user_create(self):
        user = User.objects.create(
            email = "test@gmail.com",
            username = "test user",
            bio = "test test test",
        )
        now = timezone.now()
        self.assertLess(user.date_joined, now)

    def setUp(self):
        self.test_user = User.objects.create(
            email = "test_1@testmail.com",
            username = "test_user_1",
            bio = "test test test"
        )

    def test_skill_creation(self):
        skill = Skill.objects.create(
            user = self.test_user,
            name = "Python"
        )
        self.assertIn(skill, self.test_user.skill_set.all() )
