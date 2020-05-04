import io
import os
import html

# Imports the Google Cloud client libraries
from google.api_core.exceptions import AlreadyExists
from google.cloud import vision
from google.cloud import translate_v2 as translate

def pic_to_text(infile):
    """Detects text in an image file

    ARGS
    infile: path to image file

    RETURNS
    String of text detected in image
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Opens the input image file
    with io.open(infile, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # For dense text, use document_text_detection
    # For less dense text, use text_detection
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text

    return text

def translate_text(text):
    translate_client = translate.Client()
    target = 'ro'
    translated_text = translate_client.translate(text, target_language = target)

    return translated_text

def image_to_translated_text(infile):
    text = pic_to_text(infile)
    result = translate_text(text)

    return result['translatedText']

