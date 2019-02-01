from django.core.files.temp import NamedTemporaryFile
from django.db.models import Avg

def write_image_from_url_to_disk(url):
    r = requests.get(url)
    img_tmp = NamedTemporaryFile(delete=True)
    img_tmp.write(r.content)
    img_tmp.flush()
    return img_tmp


def date_range_parser(param):
    x = param[:(param.find('-') - 1)]
    y = param[(param.find('-') + 2):]

    x = x.replace('/', '-')
    y = y.replace('/', '-')

    return x, y


def create_technique_chart(trainings):
    list_total = []

    for t in trainings:
        for f in t.forms.all():
            for tch in f.technique_assesments.all():
                list_total.append(tch.total)

    data = [
        {
            'label': 'Total Skor',
            'data': list_total
        }
    ]

    labels = ['T{}'.format(l + 1) for l in range(0, len(list_total))]

    return data, labels


def create_speed_chart(trainings):
    list_total = []
    list_movement = []

    for t in trainings:
        for f in t.forms.all():
            for spd in f.speed_assesments.all():
                list_total.append(spd.total)
                list_movement.append(spd.movement)

    data = [
        {
            'label': 'Total Skor',
            'data': list_total
        },
        {
            'label': 'Nilai Gerakan',
            'data': list_movement
        }
    ]

    labels = ['R{}'.format(l + 1) for l in range(0, len(list_total))]

    return data, labels


def create_accuracy_chart(trainings):
    list_total = []
    list_movement = []

    for t in trainings:
        for f in t.forms.all():
            for acc in f.acc_assesments.all():
                list_total.append(acc.total)
                list_movement.append(acc.movement)

    data = [
        {
            'label': 'Total Skor',
            'data': list_total
        },
        {
            'label': 'Nilai Gerakan',
            'data': list_movement
        }
    ]

    labels = ['R{}'.format(l + 1) for l in range(0, len(list_total))]

    return data, labels


def create_physic_chart(trainings):
    list_total = []

    for t in trainings:
        for f in t.forms.all():
            for phy in f.physic_assesments.all():
                list_total.append(phy.total)

    data = [
        {
            'label': 'Skor',
            'data': list_total
        }
    ]

    labels = ['L{}'.format(l + 1) for l in range(0, len(list_total))]

    return data, labels


def create_radar_chart(profile):
    accuracy_avg = tr_models.AccuracyAssesment.objects.filter(
        form__training__profile=profile,
        form__training__division=profile.level.division.name,
        form__training__level=profile.level.name,
    ).aggregate(Avg('total'))['total__avg']

    speed_avg = tr_models.SpeedAssesment.objects.filter(
        form__training__profile=profile,
        form__training__division=profile.level.division.name,
        form__training__level=profile.level.name,
    ).aggregate(Avg('total'))['total__avg']

    technique_avg = tr_models.TechniqueAssesment.objects.filter(
        form__training__profile=profile,
        form__training__division=profile.level.division.name,
        form__training__level=profile.level.name,
    ).aggregate(Avg('total'))['total__avg']

    physic_avg = tr_models.PhysicAssesment.objects.filter(
        form__training__profile=profile,
        form__training__division=profile.level.division.name,
        form__training__level=profile.level.name,
    ).aggregate(Avg('total'))['total__avg']

    return {
        'labels': ['Akurasi', 'Kecepatan', 'Teknik', 'Fisik'],
        'data': [
            float_format(accuracy_avg),
            float_format(speed_avg),
            float_format(technique_avg),
            float_format(physic_avg)
        ]
    }


def solve_division_by_zero_exception(x, y):
    if y == 0:
        return 0
    return x / y


def float_format(x):
    x = '%.1f' % x
    return float(x)
