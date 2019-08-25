from collections import Counter

from collection.models import Collection


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
