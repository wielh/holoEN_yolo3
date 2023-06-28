'''
# part1: generate image
from object_detection_program.mainUI import input_parameter_UI
input_parameter_UI()
'''

# part2: train model
from yolo3_keras.train import start_training

start_training(
    is_retrain=True, annotation_path= 'train.txt',
    model_dir_path= 'models', load_model_name= "model2.h5" ,save_model_name = 'model3.h5',
    learing_rate= 5e-6, batch_size=1, epochs=10
)

