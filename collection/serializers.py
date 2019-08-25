from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from collection.fields import RelativesField, StringBooleanField
from collection.models import Citizen, Collection


class CitizenSerializer(serializers.ModelSerializer):
    relatives = serializers.ListField()
    gender = StringBooleanField(true_value='male', false_value='female')

    class Meta:
        model = Citizen
        fields = (
            'citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives')


class CitizenCreateSerializer(CitizenSerializer):

    def validate(self, attrs):
        res = super().validate(attrs)
        citizens = self.context['request'].data['citizens']
        relatives = attrs.get('relatives')
        current_citizen_id = attrs.get('citizen_id')
        same_id_count = 0
        for cit in citizens:
            if cit['citizen_id'] == current_citizen_id:
                same_id_count += 1
                if same_id_count == 2:
                    raise ValidationError('The same citizen_id is prohibited')

        for relative in relatives:
            if relative == current_citizen_id:
                raise ValidationError('self relationships is prohibited')
            contains = False
            for other_citizen in citizens:
                if other_citizen['citizen_id'] == relative:
                    if other_citizen.get('relatives') is not None:

                        if current_citizen_id not in other_citizen['relatives']:
                            raise ValidationError('Relative have to be mutual inclusive')
                        else:
                            contains = True
                            break
                    else:
                        contains = True
                        break
            if not contains:
                raise ValidationError('Relative have to link existed citizen')

        return res


class PatchCitizenSerializer(CitizenSerializer):

    def validate(self, attrs):
        if not len(attrs) > 0:
            raise ValidationError('Empty request')
        if attrs.get('citizen_id'):
            raise ValidationError('Can not patch citizen_id')
        relatives = attrs.get('relatives')
        if relatives:
            if self.instance.citizen_id in relatives:
                raise ValidationError('The same citizen_id is prohibited')
            collection = self.instance.collection
            for relative in relatives:
                if not collection.citizens.filter(citizen_id=relative).first():
                    raise ValidationError('Relative have to be in collection')
        return super().validate(attrs)

    def update(self, instance: Citizen, validated_data):
        relatives = validated_data.pop('relatives', None)
        if relatives is not None:
            presented_relatives = instance.relatives.all()
            for presented_relative in presented_relatives:
                presented_relative.relatives.remove(instance)
                instance.relatives.remove(presented_relative)
            for relative in relatives:
                relative_object = instance.collection.citizens.get(citizen_id=relative)
                instance.relatives.add(relative_object)
                relative_object.relatives.add(instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        get_serializer = CitizenGetSerializer(instance=instance)
        return {'data': get_serializer.data}


class CitizenGetSerializer(CitizenSerializer):
    relatives = RelativesField(many=True)


class AbstractCollectionSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('citizens',)


class CollectionCreateSerializer(AbstractCollectionSerializer):
    citizens = CitizenCreateSerializer(many=True)

    def create(self, validated_data):
        collection = Collection.objects.create()
        citizens = validated_data.pop('citizens')
        created_citizens = []
        for citizen in citizens:

            relatives = citizen.pop('relatives')
            instance = Citizen(collection=collection, **citizen)
            instance.save()

            for relative in relatives:
                try:
                    relative_citizen = collection.citizens.get(citizen_id=relative)
                    instance.relatives.add(relative_citizen)
                    relative_citizen.relatives.add(instance)
                except ObjectDoesNotExist:
                    pass
            created_citizens.append(instance)

        collection.refresh_from_db()
        return collection

    #
    def to_representation(self, instance):
        result = {'data': {'import_id': instance.id}}
        return result


class CollectionShareSerializer(AbstractCollectionSerializer):
    citizens = CitizenGetSerializer(many=True)
