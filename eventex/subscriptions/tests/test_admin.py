from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin
from unittest.mock import Mock

class SubscriptionModelAdminTest(TestCase):

    def setUp(self):
        Subscription.objects.create(name='Ricardo Anzolin', cpf='12345678901',
                                    email='ricardoanzolin@gmail.com', phone='4612345789')

        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)


    def test_has_action(self):
        """Action mark_as_paid should be installed"""
        self.assertIn('mark_as_paid', self.model_admin.actions)


    def test_mark_all(self):
        """It should mark all select subscriptions as paid."""
        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        """It should send a message to the user"""
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')


    def call_action(self):
        queryset = Subscription.objects.all()
        mock = Mock()
        old_message_ser = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock
        self.model_admin.mark_as_paid(None, queryset)
        return mock