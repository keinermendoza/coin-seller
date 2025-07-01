from django.shortcuts import render
from .models import SimpleRate

def calculator(request):
    template_name = "miniclient/calculator.html"
    rates = SimpleRate.objects.select_related("base_currency", "target_currency").all()
    context = {
        "rates_dict": [rate.to_dict() for rate in rates]
    }  
    return render(request, template_name, context)