from django.contrib.auth.models import User
from django.test import TestCase

from secretsanta.models import (
    Application, SantaPair, SecretSantaConfiguration, Webhook, Year,
)


class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_webhook_model(self):
        webhook = Webhook.objects.create(name='Test Webhook', url='http://testwebhook.com')
        self.assertEqual(str(webhook), 'Test Webhook')

    def test_secretsantaconfiguration_model(self):
        config = SecretSantaConfiguration.objects.create()
        self.assertEqual(str(config), 'Secret Santa Configuration')

    def test_year_model(self):
        year = Year.objects.create(year=2023)
        self.assertEqual(year.members, 0)

    def test_application_model(self):
        year = Year.objects.create(year=2023)
        application = Application.objects.create(year=year, user=self.user1)
        self.assertEqual(application.year, year)
        self.assertEqual(application.user, self.user1)

    def test_santapair_model(self):
        year = Year.objects.create(year=2023)
        pair = SantaPair.objects.create(year=year, santa=self.user1, santee=self.user2)
        self.assertEqual(pair.year, year)
        self.assertEqual(pair.santa, self.user1)
        self.assertEqual(pair.santee, self.user2)
