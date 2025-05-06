from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import View, FormView, TemplateView, ListView
from p2p.models import FiatExchangePair, FiatExchangeDummyPairRate
from p2p.views import RequireSuperUser
from .utils import DrawImage

class ImageBannerView(RequireSuperUser, View):
    
    def get(self, request, *args, **kwargs):
        ves_brl = FiatExchangePair.objects.get(slug="ves_brl")
        brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
        ves_brl_rate = ves_brl.last_rate.rate
        brl_ves_rate = brl_ves.last_rate.rate

        image = DrawImage(
            ves_brl= f"{ves_brl_rate:.2f}",
            brl_ves=f"{brl_ves_rate:.2f}",
            date=DrawImage.get_date()
        )

        buffer = image.draw_texts()

        filename = DrawImage.generate_name()
        return HttpResponse(
            buffer,
            headers={
                "Content-Type": "image/jpeg",
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )