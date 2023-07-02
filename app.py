import argparse
from data_fetch.mainUI import input_parameter_UI
from yolo3_keras.train import start_training
# from yolo3_keras.yolo_video import start_detecting

type_of_actions = ['data_fetch','train','predict']
parser = argparse.ArgumentParser()
parser.add_argument('--action', help='要執行的動作, 選項:'+(', '.join(type_of_actions)))

parser.add_argument('--retrain', default=False)
parser.add_argument('--annotation_path')
parser.add_argument('--model_dir_path')
parser.add_argument('--load_model_name')
parser.add_argument('--save_model_name')
parser.add_argument('--learning_rate')
parser.add_argument('--batch_size')
parser.add_argument('--epochs')

parser.add_argument('--weight_path')
parser.add_argument('--classes_path')
parser.add_argument('--input_images_dir')
parser.add_argument('--output_images_dir')
args = parser.parse_args()

try:
    if args.action == 'data_fetch':
        input_parameter_UI()
    elif args.action == 'train':
        start_training(
            is_retrain = (args.retrain == "True"),
            annotation_path = args.annotation_path,
            model_dir_path=  args.model_dir_path ,
            save_model_name = args.save_model_name ,
            load_model_name= args.load_model_name,
            classes_path= args.classes_path,
            learning_rate= float(args.learning_rate),
            batch_size= int(args.batch_size),
            epochs = int(args.epochs)
        )
    '''
    elif args.action == 'predict':
        start_detecting(
            weight_path = args.weight_path,
            classes_path = args.classes_path,
            input_images_dir = args.input_images_dir,
            output_images_dir = args.output_images_dir
        )
    '''

except Exception as e:
    print("An error occurred:", str(e))
finally:
    print("Execution complete.")





'''
python app.py --action train --retrain True --model_dir_path models --save_model_name model2.h5 --load_model_name new_weight_8.h5 --classes_path yolo3_keras\model_data\voc_classes.txt  --learning_rate 1e-4 --batch_size 8 --epochs 20 --annotation_path train.txt
'''
