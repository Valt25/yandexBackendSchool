# Create your tests here.
import datetime

import numpy as np
from rest_framework.test import APITestCase

from collection.models import Collection, Citizen


class BirthdaysTestCase(APITestCase):

    def test_default(self):
        collection = Collection.objects.create(id=1)
        c1 = Citizen.objects.create(collection_id=1,
                                    citizen_id=1,
                                    town='Moscow',
                                    street='Lva Tolstogo',
                                    building='123',
                                    appartement=45,
                                    name='name',
                                    birth_date=datetime.date(1990, 7, 15),
                                    gender=True)
        c2 = Citizen.objects.create(collection_id=1,
                                    citizen_id=2,
                                    town='Moscow',
                                    street='Lva Tolstogo',
                                    building='123',
                                    appartement=45,
                                    name='name',
                                    birth_date=datetime.date(1990, 6, 15),
                                    gender=True)
        c3 = Citizen.objects.create(collection_id=1,
                                    citizen_id=3,
                                    town='Moscow',
                                    street='Lva Tolstogo',
                                    building='123',
                                    appartement=45,
                                    name='name',
                                    birth_date=datetime.date(1990, 5, 15),
                                    gender=True)
        c4 = Citizen.objects.create(collection_id=1,
                                    citizen_id=4,
                                    town='Moscow',
                                    street='Lva Tolstogo',
                                    building='123',
                                    appartement=45,
                                    name='name',
                                    birth_date=datetime.date(1990, 4, 15),
                                    gender=True)

        c1.relatives.add(c2, c3)
        c2.relatives.add(c1, c3)
        c3.relatives.add(c1, c2, c4)
        c4.relatives.add(c3)

        url = '/imports/%d/citizens/birthdays' % collection.id

        response = self.client.get(url)

        data = response.data['data']
        i = 1
        total_observed_presents = 0
        for key, value in data.items():
            self.assertEqual(i, key)
            i += 1
            for birth in value:
                self.assertNotEqual(birth['presents'], 0)
                citizen = Citizen.objects.get(collection_id=collection.id, citizen_id=birth['citizen_id'])
                presents_in_month = 0
                for relative in citizen.relatives.all():
                    if relative.birth_date.month == key:
                        presents_in_month += 1
                self.assertEqual(birth['presents'], presents_in_month)
                total_observed_presents += presents_in_month
        real_total_presents = 0
        for citizen in collection.citizens.all():
            real_total_presents += citizen.relatives.count()

        self.assertEqual(real_total_presents, total_observed_presents)


class PercentileTestCase(APITestCase):

    def test_default(self):
        collection = Collection.objects.create(id=1)
        town_name = 'Moscow'
        amount = 1399
        for i in range(1, amount):
            Citizen.objects.create(collection_id=collection.id,
                                   citizen_id=i,
                                   town=town_name,
                                   street='Lva Tolstogo',
                                   building='123',
                                   appartement=45,
                                   name='name',
                                   birth_date=datetime.date(1990 - i, 1, 1),
                                   gender=True)

        url = '/imports/%d/towns/stat/percentile/age' % collection.id
        response = self.client.get(url)
        data = response.data['data']
        result = data[0]
        ages = [29 + i for i in range(1, amount)] ## Test will be failed in next year
        self.assertEqual(result['town'], town_name)
        percentiles = np.percentile(ages, [50, 75, 99])
        self.assertEqual(result['p50'], percentiles[0])
        self.assertEqual(result['p75'], percentiles[1])
        self.assertEqual(result['p99'], percentiles[2])