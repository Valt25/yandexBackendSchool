from django.urls import path

from statistic.views import BirthdaysStatView, AgeTownPercentileView

urlpatterns = [
    path('imports/<int:pk>/citizens/birthdays', BirthdaysStatView.as_view()),
    path('imports/<int:pk>/towns/stat/percentile/age', AgeTownPercentileView.as_view()),

]