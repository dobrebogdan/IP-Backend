import textwrap

from PIL import Image, ImageDraw, ImageFont

def check_fit(text, font_fname, font_size, image_size):
    const_spacing = 4 #pixels between lines

    image_width = image_size[0]
    image_height = image_size[1]

    font = ImageFont.truetype(font_fname, size = font_size)
    char_width = font.getsize('a')[0]
    char_height = font.getsize('a')[1]
    max_chars_on_one_line = (image_width-10)//char_width
    max_lines_on_page = (image_height-10+const_spacing)//(char_height+const_spacing)
    
    split_text = text.split(sep = '\n')

    line_no = 0
    for par in split_text:
        line_no += len(textwrap.wrap(par, max_chars_on_one_line))

    if line_no > max_lines_on_page:
        return False
    return True


def binary_search_size(text, font_fname, image_size, min_size = 1, max_size = 128):
    best_size = 0
    left = min_size
    right = max_size
    while left <= right:
        mid = (left + right) // 2
        mid_check_fit = check_fit(text, font_fname, mid, image_size)
        if mid_check_fit:
            best_size = mid
            left = mid+1
        else:
            right = mid-1

    return best_size


def preprocess_text(text, font_fname, image_size):
    image_width = image_size[0]
    font_size = binary_search_size(text, font_fname, image_size)
    font = ImageFont.truetype(font_fname, size = font_size)
    char_width = font.getsize('a')[0]
    max_chars_on_one_line = image_width//char_width
    split_text = text.split(sep = '\n')
    new_text = ''
    for par in split_text:
        new_text += textwrap.fill(par, max_chars_on_one_line)
        new_text += '\n'

    return new_text, font


def text_to_image(text, font_fname = "fonts\\DejaVuSansMono.ttf", output_image_path = "my_image.jpg", size = (1166, 1600)):
    img = Image.new('RGB', (size[0], size[1]), color = (255,255,255))
    img_draw = ImageDraw.Draw(img)

    new_text, font = preprocess_text(text, font_fname, (size[0], size[1]))

    img_draw.text((10,10), new_text, font = font, fill = (0,0,0))

    img.save(output_image_path)




def main():
    text_in_ro = '''În anul 1521 la Câmpulung-Muscel, vechea capitală a Ţării Româneşti, a fost redactat primul document scris, compact şi unitar, din câte sunt cunoscute până astăzi in limba română: Scrisoarea lui Neacşu ot Dlăgopole (Câmpulung Muscel). Scrisoarea conţine un secret de mare importanţă, avertizându-l pe Johannes Benkner, judele Braşovului, despre o invazie a turcilor asupra Ardealului şi Ţării Româneşti ce tocmai se pregătea la sudul Dunării:

„Mudromu I plemenitomu, I cistitomu I bogom darovanomu jupan Hanăş Bengner ot Braşov mnogo zdravie ot Nécşu ot Dlăgopole”. (Preaînţeleptului şi cinstitului, şi de Dumnezeu dăruitului jupân Hanăş Bengner din Braşov multă sănătate din partea lui Neacşu din Câmpulung, n. n.).'''

    text_to_image(text_in_ro)



if __name__ == '__main__':
    main()