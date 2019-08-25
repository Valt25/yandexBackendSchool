from django.urls import path

from statistic.views import BirthdaysStatView

urlpatterns = [
    path('imports/<int:pk>/citizens/birthdays', BirthdaysStatView.as_view()),
]