from django.contrib import messages
from django.core import mail
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import SubscriptionForm
from django.http import HttpResponseRedirect, HttpResponse


def subscribe(request):

    if request.method == 'POST':

        form = SubscriptionForm(request.POST)


        if form.is_valid():
            form.full_clean()

            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            mail.send_mail(
                    'Confirmação de Inscrição',
                    body,
                    'contato@eventex.com',
                    ['contato@eventex.com', form.cleaned_data['email']]
            )
            message = 'Inscrição realizada com sucesso! Um email de confirmação foi enviado, não se esqueça de ' \
                      'verificar na caixa de spam.'
            messages.success(request, message)
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
    else:
        context = {'form' : SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
