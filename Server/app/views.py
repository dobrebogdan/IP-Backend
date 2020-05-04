import os.path
import uuid
import logging
from app.CreateNewImages import create_new_images
from django.http import HttpResponse

path = "images/"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lastTranslatedText = ""
shouldRetrieveImage = True

def poll(request, id):
    logger.info("POLL request received")
    if shouldRetrieveImage:
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def get(request, id):
    logger.info("GET request received")
    extension = ".jpg"
    if id == "upload":
        extension = ".bin"
    completeName = os.path.join(path, id + extension)
    with open(completeName, 'rb+') as file:
        image = file.read()
    global shouldRetrieveImage
    shouldRetrieveImage = False
    return HttpResponse(image)


def put(request):
    logger.info("PUT request received")
    if request.method == 'PUT':
        logger.info("Images creation for this request began")
        image = request.body
        (id, translated_text) = create_new_images(image)
        logger.info("The translated text is: \n" + translated_text)
        if translated_text != lastTranslatedText:
            global shouldRetrieveImage
            shouldRetrieveImage = True
        logger.info("Images creation for this request ended")
        return HttpResponse(id)
