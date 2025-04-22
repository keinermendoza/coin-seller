from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.views.generic import (
    FormView,
    TemplateView
)
from p2p.models import (
    Currency,
    CurrencyExchangeConditions,
    FiatExchangePair
)

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = "p2p/pages/react_client.html"
