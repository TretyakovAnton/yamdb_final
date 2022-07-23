from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        raise ValueError(f'Дата еще не наступила {year}')
