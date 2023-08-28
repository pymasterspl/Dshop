import datetime


def add_variable_to_context(request):

    today = datetime.date.today()
    year = today.year

    return {
        'year': year,
    }