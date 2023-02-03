from django.urls import path

from .views import ColorView, TCS320View

urlpatterns = [
    path('rgb/', ColorView.as_view()),
    path('max_rgb/', TCS320View.as_view())
]
