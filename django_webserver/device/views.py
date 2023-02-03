from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .forms import TimingForm
from .models import Device


class DeviceView(View):

    @staticmethod
    def get(request):
        form = TimingForm()
        return render(request, 'form.html', {'form': form})

    @staticmethod
    def post(request):
        dev_obj = Device.objects.all()[0]
        form = TimingForm(request.POST)
        if form.is_valid():
            on_time = form.cleaned_data.get("on_time")
            off_time = form.cleaned_data.get("off_time")

            if on_time is None:
                on_time = dev_obj.on_time
            if off_time is None:
                off_time = dev_obj.off_time

            dev_obj.on_time = on_time
            dev_obj.off_time = off_time
            dev_obj.save()
            return render(request, 'done.html', {'on_time': on_time, 'off_time': off_time})
        return HttpResponse(f"Error! Form is not valid!\n{form.errors}")


class ESP8266View(View):

    @staticmethod
    def get(request):
        dev_obj = Device.objects.all()[0]
        return HttpResponse(f"{dev_obj.on_time};{dev_obj.off_time}")
