from django.urls import path

from statistic.views import BirthdaysStatView


urlpatterns = [
    path('imports/<int:col_id>/citizens/birthdays', BirthdaysStatView.as_view()),
]