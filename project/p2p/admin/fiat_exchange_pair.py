import csv
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin, messages
from decimal import Decimal, ROUND_HALF_UP

from p2p.models import (
    FiatExchangePair,
    FiatExchangePairRate
)


@admin.register(FiatExchangePair)
class FiatExchangePairAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "par",
        "nueva_tasa",
        "rate_is_inside_min_border",
        "rate_is_inside_max_border",
        "publicado",
        "lim_max_publicado",
        "valor_mercado",
        "lim_max_mercado",
        "hora_publicado",
        "hora_mercado",
    ]

    actions = [
        "actualizar_tipo_de_cambio",
        "exportar_a_csv",
        "mostrar_tipo_de_cambio_sugerido",
    ]

    def nueva_tasa(self, obj):
        if id := obj.last_rate.id:
            app_label = FiatExchangePairRate._meta.app_label
            model_name = FiatExchangePairRate._meta.model_name
            change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[id])

            return format_html(
                f'<a href="{change_url}">Editar ultima taza</a>'
            )

    def par(self, obj):
        return f"{obj.currency_from.code}/{obj.currency_to.code}"

    def valor_mercado(self, obj):
        return obj.get_market_rate()

    def lim_max_publicado(self, obj):
        return obj.get_market_rate_plus_minimum_margin()

    def lim_max_mercado(self, obj):
        return obj.get_last_published_rate_plus_maximum_margin()

    def hora_mercado(self, obj):
        currency_from = (
            obj.currency_from.exchange_conditions.filter(
                operation_type="B",
            )
            .order_by("-created")
            .first()
        )

        if currency_from:
            return currency_from.created

    def publicado(self, obj):
        if obj.last_rate:
            return obj.last_rate.rate.quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

    def hora_publicado(self, obj):
        if obj.last_rate:
            return obj.last_rate.created

    def actualizar_tipo_de_cambio(modeladmin, request, queryset):
        for fiat_pair in queryset:
            fiat_pair.create_rate()

        modeladmin.message_user(
            request, f"nuevos tipos de cambios actualizado con exitos", messages.SUCCESS
        )
    def mostrar_tipo_de_cambio_sugerido(modeladmin, request, queryset):
        for fiat_pair in queryset:
            rate = fiat_pair.get_market_rate_plus_optimum_margin()
            modeladmin.message_user(
                request, f"{fiat_pair} usar {rate}", messages.SUCCESS
            )
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="fiat_exchange_pairs.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Par",
                "Dentro del min",
                "Dentro del max",
                "Publicado",
                "Min",
                "Valor Mercado",
                "Max",
                "Hora Publicado",
                "Hora Mercado",
            ]
        )

        for obj in queryset:
            writer.writerow(
                [
                    self.par(obj),
                    obj.rate_is_inside_min_border,
                    obj.rate_is_inside_max_border,
                    self.publicado(obj),
                    self.minimo(obj),
                    self.valor_mercado(obj),
                    self.maximo(obj),
                    self.hora_publicado(obj),
                    self.hora_mercado(obj),
                ]
            )

        return response

    exportar_a_csv.short_description = "Exportar selección a CSV"
