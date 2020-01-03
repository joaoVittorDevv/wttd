from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
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

    subscription = Subscription.objects.create(**form.cleaned_data)

    template_name = 'subscriptions/subscription_email.txt'
    subject = 'Confirmação de Inscrição'
    from_ = settings.DEFAULT_FROM_EMAIL
    to = subscription.email

    _send_email(subject, from_, to, template_name, {'subscription':subscription})

    return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))


def new(request):
     return render(request, 'subscriptions/subscription_form.html', {'form' : SubscriptionForm()})

def detail(request,pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
    return render(request, 'subscriptions/subscription_detail.html', {'subscription':subscription})


def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])