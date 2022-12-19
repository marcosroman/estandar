# utils to annotate and compose images using PIL
# (in a very basic fashion)

from PIL import Image, ImageDraw, ImageFont

# parameters
FRACTION_WIDTH_TO_COVER=0.5
STARTING_FONT_SIZE=20
FONTS_FOLDER = "/usr/share/fonts/truetype/open-sans/"
FONT_FILENAME = FONTS_FOLDER + "OpenSans-Light.ttf"
INPUT_IMG_EXTENSION = ".jpg" #?

def img_width_fraction_covered(
        img_width, width_to_annotate, font_size, font_filename):
    '''
    outputs the fraction of the image width
    that would be covered by the font
    '''
    font = ImageFont.truetype(font_filename, font_size)
    annotated_width, annotated_height = font.getsize(width_to_annotate)

    return float(annotated_width)/float(img_width)

def find_font_size(
        img_width, img_height, width_to_annotate,
        font_filename, fraction_width_to_cover):
    '''
    makes use of the bisection method to find the font size
    that will cover a given fraction of the image width
    '''
    font_size0 = STARTING_FONT_SIZE # (font sizes are always integers)
    imfc = img_width_fraction_covered(img_width, width_to_annotate,
                                      font_size0, font_filename)

    # for this, after setting font_size0 as STARTING_FONT_SIZE,
    # we seek for either the upper or lower bound of the interval that
    # contains the fontsize we want...

    # so we either keep increasing or decreasing font_size0
    # to get font_size1 and hence the interval
    if (imfc < fraction_width_to_cover):
        font_size1 = font_size0*2
        while (img_width_fraction_covered(img_width, width_to_annotate,
                                          font_size1, font_filename)
               < fraction_width_to_cover):
            font_size1=font_size1*2
    elif (imfc > fraction_width_to_cover):
        font_size1 = font_size0//2
        while (img_width_fraction_covered(img_width, width_to_annotate,
                                         font_size1, font_filename)
               > fraction_width_to_cover):
            font_size1=font_size1//2
    else:
        return font_size0

    font_size_min=min(font_size0,font_size1)
    font_size_max=max(font_size0,font_size1)
    # once we have our interval, we divide and conquer (?)
    avg_fontsize = (font_size_min+font_size_max)//2
    while ( abs(avg_fontsize-font_size_min) > 2
            and
            abs(avg_fontsize-font_size_max) > 2 ):
        imfc = img_width_fraction_covered(img_width, width_to_annotate,
                                          avg_fontsize, FONT_FILENAME)
        # if fraction covered is less than desired,
        # it must be closer to the font_size_max
        if (imfc < fraction_width_to_cover): 
            font_size_min = avg_fontsize
        # else if opposite, to the min
        elif (imfc > fraction_width_to_cover): 
            font_size_max = avg_fontsize
        else:
            return avg_fontsize
        avg_fontsize = (font_size_min+font_size_max)//2

    return avg_fontsize

def horizontal_merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    deltay = int(abs(im1.size[1]-im2.size[1])*0.5)
    # (half the difference between heights, used for centering purposes)

    if im2.size[1] > im1.size[1]:
        im.paste(im1, (0,deltay))
        im.paste(im2, (im1.size[0],0))
    else:
        im.paste(im1, (0,0))
        im.paste(im2, (im1.size[0],deltay))

    return im

def vertical_merge(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]

    im = Image.new("RGBA", (w, h))

    deltax = int(abs(im1.size[0]-im2.size[0])*0.5)
    # (half the difference between widths, used for centering purposes)

    if im2.size[0] > im1.size[0]:
        im.paste(im1, (deltax,0))
        im.paste(im2, (0,im1.size[1]))
    else:
        im.paste(im1, (0,0))
        im.paste(im2, (deltax,im1.size[1]))

    return im

def generate_annotated_images_list(input_images_folder,images_data):
    '''
    input: images_data,
             an array of dictionaries (one entry per image to annotate)
             with keys 'estandar_code' (string), width (int), height (int)
             (later we'll be ading quantity and glass_type)
    output: imageList
    '''
    INPUT_IMG_EXTENSION=".png"
    images_list = []

    for img_data in images_data:
        img_filename = (input_images_folder + "/"
                        + img_data['estandar_code']
                        + INPUT_IMG_EXTENSION)
        print("####! DEBUG: img_filename = ", img_filename)
        image = Image.open(img_filename)
        draw = ImageDraw.Draw(image)

        width, height = image.size[0], image.size[1]
        width_to_annotate = str(img_data['width'])
        height_to_annotate = str(img_data['height'])

        font_size = find_font_size(width, height, width_to_annotate, 
                                   FONT_FILENAME, FRACTION_WIDTH_TO_COVER)
        font = ImageFont.truetype(FONT_FILENAME, font_size)

        # annotate width and height:
        draw.text((width*0.5,height*0.95),width_to_annotate,
                  fill="blue",font=font,anchor="ms")
        # (width on the bottom, centered)
        draw.text((width*0.05,height*0.5),height_to_annotate,
                  fill="blue",font=font,anchor="lm")
        # (height to the left, vertically centered)

        images_list.append(image)

    return images_list

# cuidado con lo de arriba: input: images_data, an array of dictionaries with keys 'codename' (string), width (int), height (int)
def paste_images(images_list):
    '''
    # now we on we can try arrays of different sizes..
    # 1: 1
    # 2: 1 2,
    # 3: 1 2 3,
    # 4: 1 2
    #    3 4,
    # 5: 1 2 3
    #     4 5
    # 6: 1 2 3
    #    4 5 6
    '''

    assert 1<=len(images_list) and len(images_list)<=6

    if len(images_list)==1:
        return images_list[0]
    elif len(images_list)==2:
        return horizontal_merge(images_list[0],images_list[1])
    elif len(images_list)==3:
        return horizontal_merge(
                 horizontal_merge(images_list[0],images_list[1]),
                 images_list[2])
    elif len(images_list)==4:
        return vertical_merge(
                 horizontal_merge(images_list[0],images_list[1]),
                 horizontal_merge(images_list[2],images_list[3]))
    elif len(images_list)==5:
        return vertical_merge(
                 horizontal_merge(
                   horizontal_merge(images_list[0],images_list[1]),
                   images_list[2]),
                 horizontal_merge(images_list[3],images_list[4]))
    else: # ==6
        return vertical_merge(
                 horizontal_merge(
                   horizontal_merge(images_list[0],images_list[1]),
                   images_list[2]),
                 horizontal_merge(
                   horizontal_merge(images_list[3],images_list[4]),
                   images_list[5]))


def transform_detalle_planos_data(plano_detalle):
    '''
    this will receive a querylist consisting of entries in detalle_planos
    and transform the format to the 'images_data' format (list of dictionaries)
    '''

    img_data=list()
    for dp in plano_detalle:
        print('codigo.codigo=',dp.codigo.codigo)
        dpd=dict()
        dpd['estandar_code']=dp.codigo.codigo
        dpd['width']=dp.ancho_mm
        dpd['height']=dp.alto_mm
        dpd['quantity']=dp.cantidad
        dpd['type']=dp.tipo
        img_data.append(dpd)

    return img_data

def generate_and_save_plano(
        plano_id, plano_detalle,
        input_images_url, input_images_folder, output_images_folder):
    generated_image = paste_images(
                        generate_annotated_images_list(input_images_folder,
                          transform_detalle_planos_data(plano_detalle)))
    print("##!#!$$! DEBUG: now im saving")
    generated_image.save(output_images_folder+"/"+str(plano_id)+".png")

