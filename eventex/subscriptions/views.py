from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.models import Subscription
from .forms import SubscriptionForm


def subscribe(request):

    if request.method == 'POST':

        return create(request)
    elif request.method == 'GET':
        return new(request)


def create(request):

    form = SubscriptionForm(request.POST)


    if not form.is_valid():

        return render(request, 'subscriptions/subscription_form.html', {'form': form})


    template_name = 'subscriptions/subscription_email.txt'
    context = form.cleaned_data
    subject = 'Confirmação de Inscrição'
    from_ = settings.DEFAULT_FROM_EMAIL
    to = form.cleaned_data['email']

    _send_email(subject, from_, to, template_name, context)

    Subscription.objects.create(**context)

    message = 'Inscrição realizada com sucesso! Um email de confirmação foi enviado, não se esqueça de ' \
              'verificar na caixa de spam.'


    messages.success(request, message)
    return HttpResponseRedirect('/inscricao/')


def new(request):
     return render(request, 'subscriptions/subscription_form.html', {'form' : SubscriptionForm()})



def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])