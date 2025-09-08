import datetime

def give_grettings(request):
    currentTime = datetime.datetime.now()
    if 5 <= currentTime.hour < 12:
        time = 'morning'
    elif 12 <= currentTime.hour < 18:
        time = 'afternoon'
    elif 18 <= currentTime.hour < 22:
        time = 'evening'
    else:
        time = 'night'

    return {'time': time}
