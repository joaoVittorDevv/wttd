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
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        # testa se o form esta com os campos citados
        """Form must have this fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'], list(form.fields))
