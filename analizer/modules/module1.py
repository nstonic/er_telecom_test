from distutils.version import StrictVersion


def sort_and_split_errors(serialized_json: dict):
    """
    Функция сортирует список по правилам сортировки версий (2.11 больше 2.9, 2.1.11 больше 2.1.9 и т.д.),
    Поле "value" меняет строковое значение на массив из слов, удаляя все символы “ “ вокруг,
    """

    data = serialized_json.get('data')
    if not data:
        raise ValueError('No data')

    errors = [
        (error_name, error_data)
        for error_name, error_data in data.items()
    ]

    for error_name, error_data in errors:
        error_data['value'] = error_data['value'].strip()

    errors.sort(key=lambda error: StrictVersion(error[1]['ident']))
    serialized_json['data'] = dict(errors)

    return serialized_json
