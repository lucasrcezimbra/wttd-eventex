from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin
from unittest.mock import Mock

class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)
        Subscription.objects.create(name='Lucas Rangel Cezimbra', cpf='12345678901',
                                    email='lucas.cezimbra@gmail.com', phone='(51) 8210.0596')

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Subscription))

    def test_model_admin_is_registered(self):
        self.assertTrue(isinstance(self.model_admin, SubscriptionModelAdmin))

    def test_attrs(self):
        attrs = [('list_display', ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today', 'paid')),
                 ('date_hierarchy', 'created_at'),
                 ('search_fields', ('name', 'email', 'phone', 'cpf', 'created_at')),
                 ('list_filter', ('paid', 'created_at'))]

        for attr, expected in attrs:
            with self.subTest():
                self.assertEqual(expected, self.model_admin.__getattribute__(attr))

    def test_has_action(self):
        """Action mask_as_paid should be installed"""
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_as_paid_mark_all(self):
        """It should mark all selected subscriptions as paid"""
        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_mark_as_paid_message(self):
        """It should send a success message to the user"""
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def test_mark_as_paid_attr(self):
        mark_as_paid = self.model_admin.mark_as_paid
        self.assertEqual('Marcar como Pago', mark_as_paid.short_description)

    def test_subscribed_today(self):
        mock = Mock(created_at=now())
        self.assertTrue(self.model_admin.subscribed_today(mock))

    def test_subscribed_today_with_yesterday(self):
        yesterday = now() - timedelta(1)
        mock = Mock(created_at=yesterday)
        self.assertFalse(self.model_admin.subscribed_today(mock))

    def test_subscribed_today_attr(self):
        subscribed_today = self.model_admin.subscribed_today
        self.assertEqual('inscrito hoje?', subscribed_today.short_description)
        self.assertEqual(True, subscribed_today.boolean)

    def call_action(self):
        queryset = Subscription.objects.all()

        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        self.model_admin.mark_as_paid(None, queryset)

        SubscriptionModelAdmin.message_user = old_message_user

        return mock
