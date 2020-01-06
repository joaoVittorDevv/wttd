from django.db import models

class Subscription(models.Model):
    name = models.CharField('nome',max_length=60)
    cpf = models.CharField('cpf',max_length=11)
    email = models.EmailField('e-mail')
    phone = models.CharField('telefone',max_length=60)
    created_at = models.DateTimeField('criado em',auto_now_add=True)
    paid = models.BooleanField('pago',default=False)

    class Meta:
        verbose_name_plural = 'Inscrições'
        verbose_name = 'Inscrição'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name