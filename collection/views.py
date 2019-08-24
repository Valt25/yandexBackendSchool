# Create your views here.
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView

from collection.models import Collection, Citizen
from collection.serializers import CollectionCreateSerializer, CollectionShareSerializer, CitizenSerializer, \
    PatchCitizenSerializer


class CreateCollectionView(CreateAPIView):
    serializer_class = CollectionCreateSerializer
    queryset = Collection.objects.all()


class RetrieveCollectionView(RetrieveAPIView):
    serializer_class = CollectionShareSerializer
    queryset = Collection.objects.all()


class UpdateCitizenView(UpdateAPIView):
    serializer_class = PatchCitizenSerializer
    queryset = Citizen.objects.all()

    def get_object(self):
        result = self.get_queryset().filter(collection_id=self.kwargs['col_id'], citizen_id=self.kwargs['pk']).first()
        if not result:
            raise NotFound('No such citizen found')
        return result
