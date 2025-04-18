from django.shortcuts import render
from django.views.generic import (
    FormView,
    TemplateView
)

class CalculateView(TemplateView):
    template_name = "p2p/pages/calculate_form.html"
