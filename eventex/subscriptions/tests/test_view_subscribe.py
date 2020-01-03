from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription
from ..forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
    # url que esta sendo testada
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
    # codigo que ela deve retornar para ser exibida
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
    # testa se o template esta sendo exibido
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        # testa se esses elementos estao contidos no html
        """HTML must contain input tags"""

        tags = (
            ('<form', 1),
            ('<input', 6), #pois contem o hidden oculto
            ('type="text"', 3),
            ('type="email"',1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        # testa se o csrf esta presente no form
        """HTML must contain csrf middleware token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        # testa se o form está sendo exibido
        """Form is not in instance"""
        form = self.response.client.get(r('subscriptions:new')).context['form']
        self.assertIsInstance(form, SubscriptionForm)

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='João Vittor', cpf='00000000000',email='joaozao100@hotmail.com',
                     phone='47-99233-9463')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Invalid POST should not redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        """Email is being sent"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Invalid POST should not redirect to /inscricao/1/"""
        self.assertEqual(200,self.resp.status_code)

    def test_form_template(self):
        """Return form if invalid data"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
