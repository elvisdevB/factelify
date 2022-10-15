from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from app.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from  django.http import JsonResponse
from app.facturacion.models import Factura
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

class ReportVenta(LoginRequiredMixin,TemplateView):
    template_name = 'venta/reportVenta.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action =request.POST['action']
            if action == 'searchreport':
                data = []
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                search = Factura.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_emision__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.id_cliente.nombre,
                        s.fecha_emision.strftime('%Y-%m-%d'),
                        format(s.subtotal,'2f'),
                        format(s.iva,'2f'),
                        format(s.total,'2f')
                    ])
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'),0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'),0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'),0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal,'.2f'),
                    format(iva,'.2f'),
                    format(total,'.2f'),
                ])

            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Report de las ventas"
        context['entidad'] = "Reportes"
        context['list_url'] = reverse_lazy("reporte_venta")
        context['form'] = ReportForm()
        return context

