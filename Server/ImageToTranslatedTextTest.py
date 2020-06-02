import unittest
from ImageToTranslatedText import pic_to_text, translate_text

class TranslationTestCase(unittest.TestCase):

    def test_text_to_translation(self):
        result = translate_text("The quick brown fox jumps over the lazy dog")
        expected = {'translatedText': 'Vulpe brună rapidă sare peste câinele leneș', 'detectedSourceLanguage': 'en', 'input': 'The quick brown fox jumps over the lazy dog'}
        self.assertEqual(expected, result)

    def test_image_to_text(self):
        result = pic_to_text('.\\test_images\\test_image.jpg')
        expected = '''reserved for the query object. A query object that counts samples that
might become visible (because they passed the depth test) is known as an
After the queries are deleted, they are essentially gone for good. The names
of the queries can't be used again unless they are given back to you by
another call to gl GenQueries ().
Occlusion Queries
Once you've reserved your spot using gl GenQueries (), you can ask a
question. OpenGL doesn't automatically keep track of the number of
pixels it has drawn. It has to count, and it must be told when to start
counting. To do this, use glBeginQuery(). The glBeginQuery() function
takes two parameters the question you'd like to ask, and the name of the
query object that you reserved earlier:
glBeginQuery (GL_SAMPLES_PASSED, one_query);
GL SAMPLES_PASSED represents the question you're asking, "How many
samples passed the depth test?" Here, OpenGL counts samples because
you might be rendering to a multi-sampled display format, and in that
case, there could be more than one sample per pixel. In the case of a
normal, single-sampled format, there is one sample per pixel and therefore
a one-to-one mapping of samples to pixels. Every time a sample makes it
past the depth test (meaning the sample hadn't previously been discarded
by the fragment shader), OpenGL counts 1. It adds up all the samples from
all the rendering it is doing and stores the answer in part of the space
occlusion query.
dor as normal and
'''
        self.assertEqual(expected, result)