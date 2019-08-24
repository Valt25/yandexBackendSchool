from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from collection.models import Collection
from statistic.controllers import get_presents_by_month


class BirthdaysStatView(GenericAPIView):
    queryset = Collection.objects.all()

    def get(self):
        collection = self.get_object()
        return Response(data=get_presents_by_month(collection))
