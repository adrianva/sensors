from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
import csv

from sensors.models import Signal, SignalType, Sensor
import reports


def upload_csv(request):
    if request.method == 'POST':
        data = {}
        content = csv.reader(request.FILES['filebutton'])
        for row in content:
            print(row)
        data["success"] = "success"
        return HttpResponse(json.dumps(data), content_type='application/json')

    return render(request, 'upload_csv.html')


def charts(request):
    sensor_id = request.GET.get('sensor', None)
    signal_id = request.GET.get('signal', None)
    if sensor_id:
        data = {}
        signals = Signal.objects.filter(sensor_id=sensor_id, signal_id=signal_id).order_by('date')
        data['chart_data'] = reports.ChartData.convert_data_to_json(signals)

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        request = __init_session(request)
        return render(request, 'chart_test.html')


def __init_session(request):
    if "signal_types" not in request.session:
        signal_types = SignalType.objects.values_list('signal_type', flat=True).all()
        request.session["signal_types"] = list(signal_types)

    if "sensors" not in request.session:
        sensors = Sensor.objects.values_list('sensor_id', flat=True).all()
        request.session["sensors"] = list(sensors)

    return request
