from django.conf.urls import url
from sensors.views import upload_csv, charts

urlpatterns = [
    url(r'^$', upload_csv,  name='upload_csv'),
    url(r'^charts/$', charts,  name='charts'),
]
