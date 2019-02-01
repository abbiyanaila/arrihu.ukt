from datetime import date


def __get_age_by_date(_date):
    d_diff = date.today() - _date
    return d_diff.days / 365


def get_age_degrees(profiles):
    anak = 0
    remaja = 0
    dewasa = 0
    for p in profiles:
        age = __get_age_by_date(p.born_date)
        if age > 12:
            remaja += 1
        elif age > 17:
            dewasa += 1
        else:
            anak += 1
    return [
        {
            'label': 'Anak',
            'data': anak
        },
        {
            'label': 'Remaja',
            'data': remaja
        },
        {
            'label': 'Dewasa',
            'data': dewasa
        },
    ]
