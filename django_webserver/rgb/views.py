from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .forms import RGBForm
from .models import Color


def rgb_to_hex(r, g, b):
    return '{:X}{:X}{:X}'.format(r, g, b)


class ColorView(View):

    @staticmethod
    def get(request):
        dev_color = Color.objects.all()[0]
        return render(request, 'rgb.html', {'red': dev_color.red, 'green': dev_color.green, 'blue': dev_color.blue,
                                            'color': f"#{rgb_to_hex(dev_color.red, dev_color.green, dev_color.blue)}"})

    @staticmethod
    def post(request):
        dev_color = Color.objects.all()[0]
        form = RGBForm(request.POST)
        if form.is_valid():
            dev_color.red = form.cleaned_data.get("red")
            dev_color.green = form.cleaned_data.get("green")
            dev_color.blue = form.cleaned_data.get("blue")
            dev_color.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class TCS320View(View):

    @staticmethod
    def get(request):
        dev_color = Color.objects.all()[0]

        if (dev_color.red > dev_color.blue) and (dev_color.red > dev_color.green):
            res = 'R'
        elif (dev_color.blue > dev_color.green) and (dev_color.blue > dev_color.red):
            res = 'B'
        else:
            res = 'G'

        return HttpResponse(f"{res}")

