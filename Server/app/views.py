import os.path
import uuid
from django.http import HttpResponse

path = 'images/'

retrievedImages = set()

def poll(request, id):
    if id in retrievedImages:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

def get(request, id):
    completeName = os.path.join(path, id + ".jpg")
    with open(completeName, 'rb+') as file:
        image = file.read()
    retrievedImages.add(id)
    return HttpResponse(image)

def save_image(image):
    id = str(uuid.uuid1())
    completeName = os.path.join(path, id + ".jpg")
    with open(completeName, 'wb+') as file:
        file.write(image)
    return id

def put(request):
    if request.method == 'PUT':
        image = request.body
        id = save_image(image)
    return HttpResponse(id)
