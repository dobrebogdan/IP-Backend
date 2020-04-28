import os.path
from ImageProcessing.preprocess_image import TextImage
from ImageProcessing import generate_image
import ImageToTranslatedText
import logging
import uuid
path = "images/"

def create_new_images(image):
    # id = str(uuid.uuid1())
    original_id = "upload"
    cropped_id = "1"
    translated_id = "2"
    complete_original_path = os.path.join(path, original_id + ".bin")
    complete_cropped_path = os.path.join(path, cropped_id + ".jpg")
    complete_translated_path = os.path.join(path, translated_id + ".jpg")
    with open(complete_original_path, 'wb+') as file:
        file.write(image)
    try:
        cropped_text_img = TextImage(complete_original_path)
        cropped_text_img.crop_text_zone(complete_cropped_path)
        text = ImageToTranslatedText.image_to_translated_text(complete_cropped_path)
        generate_image.text_to_image(text=text, output_image_path=complete_translated_path)
    except:
        logging.error("Some images could not be created")
    return original_id
