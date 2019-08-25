# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from collection.models import Collection
from statistic.controllers import get_presents_by_month, get_percentiles_by_town


class BirthdaysStatView(GenericAPIView):
    queryset = Collection.objects.all()

    def get(self, *args, **kwargs):
        collection = self.get_object()
        return Response(data={'data': get_presents_by_month(collection)})


class AgeTownPercentileView(GenericAPIView):
    queryset = Collection.objects.all()

    def get(self, *args, **kwargs):
        collection = self.get_object()
        return Response(data={'data': get_percentiles_by_town(collection)})
