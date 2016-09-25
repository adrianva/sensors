from django.conf.urls import url
from sensors.views import upload_csv, charts, show_chart

urlpatterns = [
    url(r'^$', upload_csv,  name='upload_csv'),
    url(r'^charts/$', charts,  name='charts'),
    # TODO check if this is necessary
    url(r'^show_chart/$', show_chart,  name='show_chart'),
]
