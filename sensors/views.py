from django.shortcuts import render
from django.shortcuts import HttpResponse
import json

from sensors.models import Signal
import reports


def upload_csv(request):
    return render(request, 'upload_csv.html')


def charts(request):
    sensor_id = request.GET.get('sensor', None)
    signal_id = request.GET.get('signal', None)
    if sensor_id:
        data = {}
        signals = Signal.objects.filter(sensor_id=sensor_id, signal_id=signal_id)
        data['chart_data'] = reports.ChartData.convert_data_to_json(signals)

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form_submitted = False
        return render(request, 'chart_test.html', form_submitted)
