import time, argparse, os
from yolo3_keras.yolo import YOLO, detect_video
from pathlib import Path
from PIL import Image

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        if img.startswith("\"") and img.endswith("\""):
            img = img[1:-1]
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
        time.sleep(1)
    yolo.close_session()

def start_detecting_and_show():
    FLAGS = None
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()
    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")

# ===================================================
def start_detecting(weight_path:str, classes_path: str, input_images_dir: str, output_images_dir :str):

    yolo = YOLO(model_path=weight_path, classes_path=classes_path)
    for path in Path(input_images_dir).rglob('*.jpg'):
        try:
            image_src = os.path.join(path.parent,path.name)
            relative_path = os.path.relpath(image_src, input_images_dir)
            image_dest = os.path.join(output_images_dir,relative_path)
            image =  Image.open(image_src)
            image_out = yolo.detect_image(image)

            if not os.path.exists(os.path.dirname(image_dest)):
                os.makedirs(os.path.dirname(image_dest))
            image_out.save(image_dest)
        except Exception as e:
            print("An error happens on image:"+image_src)
            print(str(e))
            print("==================================")





