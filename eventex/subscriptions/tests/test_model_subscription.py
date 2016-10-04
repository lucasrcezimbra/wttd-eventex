from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
                name='Lucas Rangel Cezimbra',
                cpf='12345678901',
                email='lucas.cezimbra@gmail.com',
                phone='(51) 8210.0596'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Lucas Rangel Cezimbra', str(self.obj))

    def test_paid_default_to_False(self):
        """By default paid must be False"""
        self.assertFalse(self.obj.paid)
