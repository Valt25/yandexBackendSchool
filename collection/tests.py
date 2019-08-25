# Create your tests here.
import datetime

from rest_framework.test import APITestCase

from collection.models import Collection, Citizen


def citizen_object_and_models_identical(model, citizen, assert_obj):
    assert_obj.assertEqual(model.citizen_id, citizen['citizen_id'])
    assert_obj.assertEqual(model.town, citizen['town'])
    assert_obj.assertEqual(model.street, citizen['street'])
    assert_obj.assertEqual(model.building, citizen['building'])
    assert_obj.assertEqual(model.apartment, citizen['apartment'])
    assert_obj.assertEqual(model.name, citizen['name'])
    assert_obj.assertEqual(model.birth_date, datetime.datetime.strptime(citizen['birth_date'], '%d.%m.%Y').date())
    assert_obj.assertEqual(model.gender, citizen['gender'] == 'male')
    assert_obj.assertEqual(model.relatives.count(), len(citizen['relatives']))
    assert_obj.assertEqual(list(map(lambda rel: rel.citizen_id, model.relatives.all())), citizen['relatives'])


class CollectionCreateTestCase(APITestCase):
    url = '/import'

    def test_create_with_single_citizen(self):
        citizen = {
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": []
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        collection = Collection.objects.last()
        self.assertEqual(response.data['data']['import_id'], collection.id)
        citizen_obj = collection.citizens.get(citizen_id=citizen['citizen_id'])
        citizen_object_and_models_identical(citizen_obj, citizen, self)

    def test_create_with_single_fail_blank_name(self):
        citizen = {
            "citizen_id": 1,
            "town": "",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": [2, 28]
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_normal(self):
        data = {'citizens': [{
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": [2, 28]},
            {
                "citizen_id": 2,
                "town": "Алма-Ата",
                "street": "Кажымукана",
                "building": "26",
                "apartment": 5,
                "name": "Валерий Валерьяновичь Валерьевич",
                "birth_date": "29.09.1996",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 28,
                "town": "Казань",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 71,
                "name": "Иванов Генадий Васильевич",
                "birth_date": "20.07.2000",
                "gender": "male",
                "relatives": [1]
            }
        ]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        collection = Collection.objects.last()
        self.assertEqual(response.data['data']['import_id'], collection.id)

    def test_same_citizen_id_in_collection(self):
        data = {'citizens': [{
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": []},
            {
                "citizen_id": 1,
                "town": "Алма-Ата",
                "street": "Кажымукана",
                "building": "26",
                "apartment": 5,
                "name": "Валерий Валерьяновичь Валерьевич",
                "birth_date": "29.09.1996",
                "gender": "male",
                "relatives": []
            },
            {
                "citizen_id": 1,
                "town": "Казань",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 71,
                "name": "Иванов Генадий Васильевич",
                "birth_date": "20.07.2000",
                "gender": "male",
                "relatives": []
            }
        ]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_fail_relations(self):
        data = {'citizens': [{
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": [2, 28]},
            {
                "citizen_id": 2,
                "town": "Алма-Ата",
                "street": "Кажымукана",
                "building": "26",
                "apartment": 5,
                "name": "Валерий Валерьяновичь Валерьевич",
                "birth_date": "29.09.1996",
                "gender": "male",
                "relatives": []
            },
            {
                "citizen_id": 28,
                "town": "Казань",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 71,
                "name": "Иванов Генадий Васильевич",
                "birth_date": "20.07.2000",
                "gender": "male",
                "relatives": [1]
            }
        ]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_undefined_field(self):
        citizen = {
            "citizen_id": 1,
            "town": "",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": [2, 28]
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_undefined_relatives_field(self):
        citizen = {
            "citizen_id": 1,
            "town": "qwe",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 1,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male"
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_undefined_relatives_in_pack(self):
        citizen1 = {
            "citizen_id": 1,
            "town": "123",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 5,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male"
        }
        citizen2 = {
            "citizen_id": 2,
            "town": "Алма-Ата",
            "street": "Кажымукана",
            "building": "26",
            "apartment": 5,
            "name": "Валерий Валерьяновичь Валерьевич",
            "birth_date": "29.09.1996",
            "gender": "male",
            "relatives": [1]
        }

        citizen3 = {
            "citizen_id": 3,
            "town": "Алма-Ата",
            "street": "Кажымукана",
            "building": "26",
            "apartment": 5,
            "name": "Валерий Валерьяновичь Валерьевич",
            "birth_date": "29.09.1996",
            "gender": "male",
            "relatives": [1]
        }
        data = {'citizens': [citizen1, citizen2, citizen3]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_unneded_field(self):
        citizen = {
            "citizen_id": 1,
            "town": "qwe",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 5,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2000",
            "gender": "male",
            "relatives": [],
            "more": 123
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_future_birthdate(self):
        citizen = {
            "citizen_id": 1,
            "town": "qwe",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 5,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.02.2123",
            "gender": "male",
            "relatives": [],
        }
        data = {'citizens': [citizen]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)


class CollectionGetTestCase(APITestCase):

    def setUp(self) -> None:
        Collection.objects.create(id=1)
        Citizen.objects.create(collection_id=1,
                               citizen_id=1,
                               town='Moscow',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True)

        Collection.objects.create(id=2)
        Citizen.objects.create(collection_id=2,
                               citizen_id=1,
                               town='Moscow',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )
        Citizen.objects.create(collection_id=2,
                               citizen_id=2,
                               town='Moscow',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )
        Citizen.objects.create(collection_id=2,
                               citizen_id=3,
                               town='Moscow',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )

    def test_get_citizens(self):
        collections = Collection.objects.all()
        for collection in collections:
            url = '/imports/%d/citizens' % collection.id
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, 200)
            response_citizens = response.data['data']
            for citizen in response_citizens:
                citizen_obj = collection.citizens.get(citizen_id=citizen['citizen_id'])
                citizen_object_and_models_identical(citizen_obj, citizen, self)


class CitizenPatchTestCase(APITestCase):

    def setUp(self) -> None:
        Collection.objects.create(id=1)
        Citizen.objects.create(collection_id=1,
                               citizen_id=1,
                               town='Moscow',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True)

        Citizen.objects.create(collection_id=1,
                               citizen_id=2,
                               town='Moscow1',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )
        Citizen.objects.create(collection_id=1,
                               citizen_id=3,
                               town='Moscow2',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )
        Citizen.objects.create(collection_id=1,
                               citizen_id=4,
                               town='Moscow3',
                               street='Lva Tolstogo',
                               building='123',
                               apartment=45,
                               name='name',
                               birth_date=datetime.datetime(1990, 5, 15),
                               gender=True
                               )

    def test_plain_entity_patch(self):
        citizen = Citizen.objects.first()
        url = '/imports/%d/citizens/%d' % (citizen.collection_id, citizen.citizen_id)
        data = {
            'name': 'new name'
        }
        response = self.client.patch(url, data, format='json')
        citizen_resp = response.data['data']
        citizen.refresh_from_db()
        for key, value in data.items():
            self.assertEqual(citizen_resp[key], data[key])
        citizen_object_and_models_identical(citizen, citizen_resp, self)

    def test_change_relationships_patch(self):
        collection = Collection.objects.first()

        original_citizen = collection.citizens.get(citizen_id=1)
        related_citizen = collection.citizens.get(citizen_id=2)
        url = '/imports/%d/citizens/%d' % (original_citizen.collection_id, original_citizen.citizen_id)
        data = {
            'relatives': [related_citizen.citizen_id]
        }
        response = self.client.patch(url, data, format='json')
        citizen_resp = response.data['data']
        original_citizen.refresh_from_db()
        related_citizen.refresh_from_db()
        self.assertTrue(related_citizen in original_citizen.relatives.all())
        self.assertTrue(original_citizen in related_citizen.relatives.all())

        for key, value in data.items():
            self.assertEqual(citizen_resp[key], data[key])
        citizen_object_and_models_identical(original_citizen, citizen_resp, self)

    def test_empty_request(self):
        collection = Collection.objects.first()
        original_citizen = collection.citizens.get(citizen_id=1)
        data = {}
        url = '/imports/%d/citizens/%d' % (original_citizen.collection_id, original_citizen.citizen_id)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_change_citizen_id(self):
        collection = Collection.objects.first()
        original_citizen = collection.citizens.get(citizen_id=1)
        data = {
            'citizen_id': 2
        }
        url = '/imports/%d/citizens/%d' % (original_citizen.collection_id, original_citizen.citizen_id)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_empty_field(self):
        collection = Collection.objects.first()
        original_citizen = collection.citizens.get(citizen_id=1)
        data = {
            'name': ''
        }
        url = '/imports/%d/citizens/%d' % (original_citizen.collection_id, original_citizen.citizen_id)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_relate_self(self):
        collection = Collection.objects.first()
        original_citizen = collection.citizens.get(citizen_id=1)
        data = {
            'relatives': [original_citizen.citizen_id]
        }
        url = '/imports/%d/citizens/%d' % (original_citizen.collection_id, original_citizen.citizen_id)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
