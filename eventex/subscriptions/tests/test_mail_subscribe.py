from django.test import TestCase
from django.core import mail


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='João Vittor', cpf='00000000000',email='joaozao100@hotmail.com',
                     phone='47-99233-9463')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_sender(self):

        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):

        expect = ['contato@eventex.com', 'joaozao100@hotmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):

        contents = [
            'João Vittor',
            '00000000000',
            'joaozao100@hotmail.com',
            '47-99233-9463',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)