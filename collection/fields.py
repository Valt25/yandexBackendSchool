from rest_framework.fields import Field
from rest_framework.relations import RelatedField


class RelativesField(RelatedField):
    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        return int(value.citizen_id)


class StringBooleanField(Field):

    def __init__(self, **kwargs):
        super().__init__()
        self.true_value = kwargs['true_value']
        self.false_value = kwargs['false_value']

    def to_internal_value(self, data):
        return data == self.true_value

    def to_representation(self, value):
        return self.true_value if value else self.false_value