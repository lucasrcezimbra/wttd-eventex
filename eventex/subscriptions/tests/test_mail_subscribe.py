from django.test import TestCase
from django.core import mail

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Lucas Rangel Cezimbra', cpf='12345678901',
                    email='lucas.cezimbra@gmail.com', phone='(51) 8899.7766')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'lucas.cezimbra@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ('Lucas Rangel Cezimbra',
                    '12345678901',
                    'lucas.cezimbra@gmail.com',
                    '(51) 8899.7766')

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
