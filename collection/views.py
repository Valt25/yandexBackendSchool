# Create your views here.
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response

from collection.models import Collection, Citizen
from collection.serializers import CollectionCreateSerializer, PatchCitizenSerializer, CitizenGetSerializer


class CreateCollectionView(CreateAPIView):
    serializer_class = CollectionCreateSerializer
    queryset = Collection.objects.all()


class RetrieveCollectionView(GenericAPIView):
    serializer_class = CitizenGetSerializer
    queryset = Collection.objects.all()

    def get(self, *args, **kwargs):
        instance = self.get_object()
        citizens = instance.citizens.all()
        serializer = self.get_serializer(citizens, many=True)
        return Response(data={'data': serializer.data})


class UpdateCitizenView(UpdateAPIView):
    serializer_class = PatchCitizenSerializer
    queryset = Citizen.objects.all()

    def get_object(self):
        result = self.get_queryset().filter(collection_id=self.kwargs['col_id'], citizen_id=self.kwargs['pk']).first()
        if not result:
            raise NotFound('No such citizen found')
        return result
