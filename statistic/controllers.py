from collections import Counter

import numpy as np

from collection.models import Collection
from statistic.utils import get_age


def get_presents_by_month(collection: Collection):
    results_per_citizen = []
    for citizen in collection.citizens.all():
        citizen_result = Counter()
        for relative in citizen.relatives.all():
            month = relative.birth_date.month
            citizen_result[month] += 1
        results_per_citizen.append((citizen.citizen_id, citizen_result))
    result = {}
    for i in range(1, 12):
        month_result = []
        for citizen_id, citizen_result in results_per_citizen:
            if citizen_result[i] > 0:
                month_result.append({'citizen_id': citizen_id, 'presents': citizen_result[i]})
        result[i] = month_result
    return result


def get_percentiles_by_town(collection: Collection):
    towns = collection.citizens.values_list('town', flat=True).distinct()
    result = []
    for town in towns:
        citizens = collection.citizens.filter(town=town)
        citizen_ages = []
        for citizen in citizens:
            citizen_ages.append(get_age(citizen.birth_date))
        res = np.percentile(citizen_ages, [50, 75, 99])
        result.append({'town': town, 'p50': res[0], 'p75': res[1], 'p99': res[2]})
    return result
