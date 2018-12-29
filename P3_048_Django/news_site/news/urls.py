from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.reports, name='reports'),
    url(r'^(?P<report_id>\d+)/$', views.reports_detail, name='reports_detail')
]
