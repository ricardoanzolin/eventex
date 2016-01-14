from django.test import TestCase
from django.core import mail

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Ricardo Anzolin', cpf='12345678901', email='ricardoanzolin@gmail.com', phone='4684098444')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br','ricardoanzolin@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Ricardo Anzolin',
            '12345678901',
            'ricardoanzolin@gmail.com',
            '4684098444',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)