# Image Processing

## Setup

Before using these modules you should install all prerequisites. For this, you can run the following command:

    pip install -r requirements.txt

## Generate Image with a Given Text

Given a text we generate an image having a white background with that text. The font size is automatically calculated so the text fits perfectly in the image.

The current font we used is DejaVuSansMono font. This can easily be changed, bearing in mind that the font needs to be monospaced (otherwise, we offer no guarantee that the text will fit in the image).

### Usage in a python script:

First, import the generate_image module.

	import generate_image

Then you can use the text_to_image function from the module like this:

	generate_image.text_to_image(your_text)

This method will create the image and save it as 'my_image.jpg'.

For a more particular use case, you could use the function like this:

    generate_image.text_to_image(your_text, path_to_your_font, output_image_path, output_image_size)

You can also run the generate_image.py script to view an example.


## Preprocess Image (Crop)

Given an image with some text, we get the cropped image focused on the text. It doesn't matter in which format is the image stored.

### Usage in a python script:

First, import the preprocess_image module.

    import preprocess_image

Then, create an instance of the TextImage class like this:

    img = TextImage(path_to_your_image)

You can use crop_text_zone() method to save the cropped image to a given path:

    img.crop_text_zone(path_to_output_image)

You can also run the preprocess_image.py script to view some examples (see the inputs and results folders).