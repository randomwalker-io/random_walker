import numpy
import json
import django

def generateDestination(request):
    if request.method == 'POST':
        current_location = request.POST.get('current_location')
        
    with open('debug.txt', 'w') as f:
        f.write(current_location)
        
    # current_location is of the form (u'lat': 123, u'lng': 456)
    radius = 0.2
    numberdestin = 1
    
    # create shift, angle is in radian
    angle = numpy.random.uniform(low=0, high=1, size=numberdestin) * 2 * numpy.pi
    lat_shift = float(numpy.cos(angle) * radius)
    lng_shift = float(numpy.sin(angle) * radius)
    new_lat = current_location['lat'] + lat_shift
    new_lng = current_location['lng'] + lng_shift

    # Create new destination
    new_destination = {'lat': new_lat, 'lng': new_lng}
    # return HttpResponse(
    #     json.dumps(new_destination),
    #     content_type='application/json'
    # )
    # return JsonResponse(new_destination)
    return current_location




# tmp = {u'lat': 123, u'lng': 456}
# new_destination = generateDestination(tmp);
# print new_destination

