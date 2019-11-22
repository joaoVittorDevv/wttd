from django.core import mail
from django.test import TestCase
from .forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
    # url que esta sendo testada
        self.response = self.client.get('/inscricao/')

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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6) # 6 pois o csrf é um input hidden
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        # testa se o csrf esta presente no form
        """HTML must contain csrf middleware token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        # testa se o form está sendo exibido
        """Form is not in instance"""
        form = self.response.client.get('/inscricao/').context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        # testa se o form esta com os campos citados
        """Form must have this fields"""
        form = self.response.client.get('/inscricao/').context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='João Vittor', cpf='00000000000',email='joaozao100@hotmail.com',
                     phone='47-99233-9463')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302,self.resp.status_code)
    def test_send_subscribe_email(self):
        """Email is being sent"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_sender(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com', 'joaozao100@hotmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('João Vittor', email.body)
        self.assertIn('00000000000', email.body)
        self.assertIn('joaozao100@hotmail.com', email.body)
        self.assertIn('47-99233-9463', email.body)

class SubscribeInvalidPost(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_form_template(self):
        """Return form if invalid data"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='João Vittor', cpf='00000000000',email='joaozao100@hotmail.com',
                     phone='47-99233-9463')
        response = self.client.post('/inscricao/', data, follow=True)
        expect =  'Inscrição realizada com sucesso! Um email de confirmação foi enviado, não se esqueça de ' \
                  'verificar na caixa de spam'
        self.assertContains(response, expect)