import datetime


def get_age(birth_date):
    today = datetime.datetime.utcnow().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))