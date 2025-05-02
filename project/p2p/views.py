from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import View, FormView, TemplateView, ListView
from p2p.models import FiatExchangePair, FiatExchangeDummyPairRate

class RequireSuperUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = "p2p/pages/react_client.html"

class SetRatesView(RequireSuperUser, ListView):
    template_name = "p2p/pages/set_rates_view.html"
    queryset = FiatExchangeDummyPairRate.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.get('slug', 'brl_ves')
        queryset.filter(slug=slug)

    def get(self, request, *args, **kwargs):
        pass
    
    def post(self, request, *args, **kwargs):
        pass
