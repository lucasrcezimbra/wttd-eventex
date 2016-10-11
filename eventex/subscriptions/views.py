from django.views.generic import DetailView
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from eventex.subscriptions.mixins import EmailCreateView

new = EmailCreateView.as_view(model=Subscription,
                              form_class=SubscriptionForm,
                              email_subject='Confirmação de Inscrição')

detail = DetailView.as_view(model=Subscription)
