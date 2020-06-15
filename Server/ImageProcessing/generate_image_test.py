import unittest
from generate_image import check_fit, binary_search_size, preprocess_text
from PIL import ImageFont

class GenerateImageTestCase(unittest.TestCase):
    def test_check_fit(self):
        text = '''În anul 1521 la Câmpulung-Muscel, vechea capitală a Ţării Româneşti, a fost redactat primul document scris, compact şi unitar, din câte sunt cunoscute până astăzi in limba română: Scrisoarea lui Neacşu ot Dlăgopole (Câmpulung Muscel). Scrisoarea conţine un secret de mare importanţă, avertizându-l pe Johannes Benkner, judele Braşovului, despre o invazie a turcilor asupra Ardealului şi Ţării Româneşti ce tocmai se pregătea la sudul Dunării:

„Mudromu I plemenitomu, I cistitomu I bogom darovanomu jupan Hanăş Bengner ot Braşov mnogo zdravie ot Nécşu ot Dlăgopole”. (Preaînţeleptului şi cinstitului, şi de Dumnezeu dăruitului jupân Hanăş Bengner din Braşov multă sănătate din partea lui Neacşu din Câmpulung, n. n.).'''
        font_name = 'fonts\DejaVuSansMono.ttf'
        font_size = 32
        image_size = (1166, 1600)
        actual = check_fit(text, font_name, font_size, image_size)
        expected = True
        self.assertEquals(actual, expected)
        text = '''În anul 1521 la Câmpulung-Muscel, vechea capitală a Ţării Româneşti, a fost redactat primul document scris, compact şi unitar, din câte sunt cunoscute până astăzi in limba română: Scrisoarea lui Neacşu ot Dlăgopole (Câmpulung Muscel). Scrisoarea conţine un secret de mare importanţă, avertizându-l pe Johannes Benkner, judele Braşovului, despre o invazie a turcilor asupra Ardealului şi Ţării Româneşti ce tocmai se pregătea la sudul Dunării:

    „Mudromu I plemenitomu, I cistitomu I bogom darovanomu jupan Hanăş Bengner ot Braşov mnogo zdravie ot Nécşu ot Dlăgopole”. (Preaînţeleptului şi cinstitului, şi de Dumnezeu dăruitului jupân Hanăş Bengner din Braşov multă sănătate din partea lui Neacşu din Câmpulung, n. n.).'''
        font_name = 'fonts\DejaVuSansMono.ttf'
        font_size = 64
        image_size = (1166, 1600)
        actual = check_fit(text, font_name, font_size, image_size)
        expected = False
        self.assertEquals(actual, expected)

    def test_binary_search(self):
        text = '''În anul 1521 la Câmpulung-Muscel, vechea capitală a Ţării Româneşti, a fost redactat primul document scris, compact şi unitar, din câte sunt cunoscute până astăzi in limba română: Scrisoarea lui Neacşu ot Dlăgopole (Câmpulung Muscel). Scrisoarea conţine un secret de mare importanţă, avertizându-l pe Johannes Benkner, judele Braşovului, despre o invazie a turcilor asupra Ardealului şi Ţării Româneşti ce tocmai se pregătea la sudul Dunării:

        „Mudromu I plemenitomu, I cistitomu I bogom darovanomu jupan Hanăş Bengner ot Braşov mnogo zdravie ot Nécşu ot Dlăgopole”. (Preaînţeleptului şi cinstitului, şi de Dumnezeu dăruitului jupân Hanăş Bengner din Braşov multă sănătate din partea lui Neacşu din Câmpulung, n. n.).'''
        font_name = 'fonts\DejaVuSansMono.ttf'
        min_size = 1
        max_size = 128
        image_size = (1166, 1600)
        actual = binary_search_size(text, font_name, image_size, min_size, max_size)
        expected = 60
        self.assertEquals(actual, expected)

    def test_preprocess_text(self):
        text = '''În anul 1521 la Câmpulung-Muscel, vechea capitală a Ţării Româneşti, a fost redactat primul document scris, compact şi unitar, din câte sunt cunoscute până astăzi in limba română: Scrisoarea lui Neacşu ot Dlăgopole (Câmpulung Muscel). Scrisoarea conţine un secret de mare importanţă, avertizându-l pe Johannes Benkner, judele Braşovului, despre o invazie a turcilor asupra Ardealului şi Ţării Româneşti ce tocmai se pregătea la sudul Dunării:

„Mudromu I plemenitomu, I cistitomu I bogom darovanomu jupan Hanăş Bengner ot Braşov mnogo zdravie ot Nécşu ot Dlăgopole”. (Preaînţeleptului şi cinstitului, şi de Dumnezeu dăruitului jupân Hanăş Bengner din Braşov multă sănătate din partea lui Neacşu din Câmpulung, n. n.).'''
        font_name = 'fonts\DejaVuSansMono.ttf'
        image_size = (1166, 1600)

        actual = preprocess_text(text, font_name, image_size)
        font_size = 60
        font = ImageFont.truetype(font_name, size=font_size)
        new_text = '''În anul 1521 la Câmpulung-
Muscel, vechea capitală a Ţării
Româneşti, a fost redactat
primul document scris, compact
şi unitar, din câte sunt
cunoscute până astăzi in limba
română: Scrisoarea lui Neacşu ot
Dlăgopole (Câmpulung Muscel).
Scrisoarea conţine un secret de
mare importanţă, avertizându-l
pe Johannes Benkner, judele
Braşovului, despre o invazie a
turcilor asupra Ardealului şi
Ţării Româneşti ce tocmai se
pregătea la sudul Dunării:

„Mudromu I plemenitomu, I
cistitomu I bogom darovanomu
jupan Hanăş Bengner ot Braşov
mnogo zdravie ot Nécşu ot
Dlăgopole”. (Preaînţeleptului şi
cinstitului, şi de Dumnezeu
dăruitului jupân Hanăş Bengner
din Braşov multă sănătate din
partea lui Neacşu din Câmpulung,
n. n.).
'''
        expected = (new_text, font)
        self.assertEqual(actual[0], expected[0])
        self.assertEqual(actual[1].getname(), expected[1].getname())
