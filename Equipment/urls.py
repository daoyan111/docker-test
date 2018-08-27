from django.conf.urls import url
from Equipment.views import eqList, eqDatas, equip_api, gateone


urlpatterns = [
    url(r'^eqList/$', eqList, name='eqList'),
    url(r'^$', eqList, name='eqList'),
    url(r'eqDatas/(\d+)', eqDatas),
    url(r'equip_api/$', equip_api),
    url(r'gateone/$', gateone),
]