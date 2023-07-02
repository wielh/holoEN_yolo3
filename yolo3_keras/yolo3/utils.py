"""Miscellaneous utility functions."""

from functools import reduce
from PIL import Image
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

def compose(*funcs):
    """Compose arbitrarily many functions, evaluated left to right.

    Reference: https://mathieularose.com/function-composition-in-python/
    """
    # return lambda x: reduce(lambda v, f: f(v), funcs, x)
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')

def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    '''
    cv2.INTER_LINEAR	The standard bilinear interpolation, ideal for enlarged images.
    cv2.INTER_NEAREST	The nearest neighbor interpolation, which, though fast to run,
                        creates blocky images.
    cv2.INTER_AREA	    The interpolation for the pixel area, which scales down images.
    cv2.INTER_CUBIC	    The bicubic interpolation with 4×4-pixel neighborhoods, which,
                        though slow to run, generates high-quality instances.
    cv2.INTER_LANCZOS4	The Lanczos interpolation with an 8×8-pixel neighborhood,
                        which generates images of the highest quality but is the slowest to run.
    '''
    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128,128,128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image

def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a

def get_random_data(annotation_line, input_shape,
    random=True, max_boxes=20, jitter=.2, hue=0.2, sat=1.2, val=1.2, proc_img=True):
    '''random preprocessing for real-time data augmentation'''

    # jitter:　resize image factor
    # hue: pixel value translate factor
    # val: pixel brightness factor

    annotation_line = annotation_line.replace("\n","")
    try:
        image_path, line = annotation_line.split(sep="<PathEnd>",maxsplit=1)
        line = line.split(" ")[1:]

        image = Image.open(image_path)
        input_width, input_height = image.size
        model_shape_width, model_shape_height = input_shape
        box = np.array([np.array(list(map(int,bo.split(',')))) for bo in line])

        if not random:
            # resize image
            scale = min(model_shape_width/input_width, model_shape_height/input_height)
            new_model_shape_width = int(input_width*scale)
            new_model_shape_height  = int(input_height*scale)
            dx = (model_shape_width-new_model_shape_width)//2
            dy = (model_shape_height-new_model_shape_height)//2
            image_data=0
            if proc_img:
                image = image.resize((new_model_shape_width,new_model_shape_height), Image.BICUBIC)
                new_image = Image.new('RGB', (model_shape_width,model_shape_height), (128,128,128))
                new_image.paste(image, (dx, dy))
                image_data = np.array(new_image)/255.

            # correct boxes
            box_data = np.zeros((max_boxes,5))
            if len(box)>0:
                np.random.shuffle(box)
                if len(box)>max_boxes: box = box[:max_boxes]
                box[:, [0,2]] = box[:, [0,2]]*scale + dx
                box[:, [1,3]] = box[:, [1,3]]*scale + dy
                box_data[:len(box)] = box

            return image_data, box_data
        else:
            # resize image w.r.t. ratio of height and width
            new_ar = model_shape_width/model_shape_height * rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter)
            # scale = rand(.8, 1.2)
            if new_ar < 1:
                new_model_shape_height = int(model_shape_height)
                new_model_shape_width = int(new_model_shape_height*new_ar)
                #  new_model_shape_width = int(model_shape_width* rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter))
            else:
                new_model_shape_width = int(model_shape_width)
                new_model_shape_height = int(model_shape_width/new_ar)
                # new_model_shape_height = int(model_shape_height* rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter))
            image = image.resize((new_model_shape_width,new_model_shape_height), Image.BICUBIC)

            # place image (OK)
            dx = int(rand(0, model_shape_width-new_model_shape_width))
            dy = int(rand(0, model_shape_height-new_model_shape_height))
            new_image = Image.new('RGB', (model_shape_width,model_shape_height), (128,128,128))
            new_image.paste(image, (dx, dy))
            image = new_image

            # flip image or not (OK)
            flip = rand()<.5
            if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # distort image
            hue = rand(-hue, hue)
            sat = rand(1, sat) if rand()<.5 else 1/rand(1, sat)
            val = rand(1, val) if rand()<.5 else 1/rand(1, val)
            image_hsv = rgb_to_hsv(np.array(image)/255.)
            image_hsv[..., 0] += hue   # pixel value translate, numpy array, 0 to 1
            image_hsv[..., 0][image_hsv[..., 0]>1] -= 1
            image_hsv[..., 0][image_hsv[..., 0]<0] += 1
            image_hsv[..., 1] *= sat  # pixel saturation translate
            image_hsv[..., 2] *= val  # pixel brightness translate
            image_hsv[image_hsv>1] = 1
            image_hsv[image_hsv<0] = 0
            image_data = hsv_to_rgb(image_hsv)

            # correct boxes x,y,z,w w.r.t new_input_width and new_input_height
            box_data = np.zeros((max_boxes,5))
            if len(box)>0:
                np.random.shuffle(box)
                # box left_top_x, left_top_y, bottom_right_x, bottom_right_y, class_index
                box[:, [0,2]] = box[:, [0,2]]*new_model_shape_width/input_width + dx
                box[:, [1,3]] = box[:, [1,3]]*new_model_shape_height/input_height + dy
                if flip: box[:, [0,2]] = model_shape_width - box[:, [2,0]]
                box[:, 0:2][box[:, 0:2]<0] = 0
                box[:, 2][box[:, 2]>model_shape_width] = model_shape_width
                box[:, 3][box[:, 3]>model_shape_height] = model_shape_height
                box_w = box[:, 2] - box[:, 0]
                box_h = box[:, 3] - box[:, 1]
                box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box
                if len(box)>max_boxes: box = box[:max_boxes]
                box_data[:len(box)] = box

            return image_data, box_data
    except:
        print("annotation_line:"+ annotation_line)
