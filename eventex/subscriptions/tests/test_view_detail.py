from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):

    def setUp(self):
        self.obj = Subscription.objects.create(
            name='João Vittor',
            cpf='00000000000',
            email='joaozao100@hotmail.com',
            phone='47-99233-9463'
        )

        self.resp = self.client.get(r('subscriptions:detail', self.obj.pk))
    def test_get(self):
        self.assertEqual(200, self.resp.status_code)
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription,Subscription)
    def test_html(self):
        content = (self.obj.name, self.obj.email,self.obj.cpf, self.obj.phone)

        with self.subTest():
            for content in content:
                self.assertContains(self.resp, content)

class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('subscriptions:detail', 0))
        self.assertEquals(404, resp.status_code )
