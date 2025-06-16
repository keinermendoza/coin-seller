from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import View, FormView, TemplateView, ListView
from p2p.models import FiatExchangePair, FiatExchangeDummyPairRate

class RequireSuperUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = "p2p/pages/react_client.html"

