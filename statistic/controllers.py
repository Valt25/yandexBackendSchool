from collection.models import Collection


def get_presents_by_month(collection: Collection):
    result = {i: [] for i in range(1, 12)}
    return result
