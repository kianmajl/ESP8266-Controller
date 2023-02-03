from django.urls import path

from .views import DeviceView, ESP8266View

urlpatterns = [
    path('time/', DeviceView.as_view()),
    path('get/', ESP8266View.as_view())
]