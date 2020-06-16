import os.path
from ImageProcessing.preprocess_image import TextImage
from ImageProcessing import generate_image
from TextClassification.TextClassifier import TextClassifier
import ImageToTranslatedText
import logging
import traceback
import uuid
path = "images/"
logging.basicConfig()

def create_new_images(image):
    # id = str(uuid.uuid1())
    text = ""
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
        logging.info("Original path:" + complete_original_path)
        logging.info("Cropped path: " + complete_cropped_path)
        cropped_text_img.crop_text_zone(complete_cropped_path)
        text = ImageToTranslatedText.image_to_translated_text(complete_cropped_path)

        data_set_path = os.path.join("TextClassification", "data", "bbc")
        classifier = TextClassifier.getTextClassifier(data_set_path)
        classname = classifier.predictTexts([text])[0]
        text = classname[0] + '\n'+'\n'+text
        generate_image.text_to_image(text=text, output_image_path=complete_translated_path)
        logging.info("All images were created")
    except Exception as exception:
        logging.error("Some images could not be created because of the following exception\n" + str(exception))
        traceback.print_exc()
    return original_id, text
