from tensorflow.keras.optimizers import SGD
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import os

classes_path = 'yolo3_keras/model_data/voc_classes.txt'
anchors_path = 'yolo3_keras/model_data/yolo_anchors.txt'
default_save_weight_path = 'yolo3_keras/model_data/yolo_weights.h5'
default_save_tiny_weight_path = 'yolo3_keras/model_data/tiny_yolo_weights.h5'

seed = 69420
val_split = 0.1

def get_callbacks(log_dir):
    logging = TensorBoard(log_dir=log_dir)
    checkpoint = ModelCheckpoint(
        os.path.join(log_dir,'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5'),
        monitor='val_loss', save_weights_only=True, save_best_only=True, period=3)
    early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=5, verbose=1)
    return [logging, checkpoint, reduce_lr, early_stopping]

def get_optimizer(learning_rate = 1e-5):
    return SGD(lr = learning_rate)

'''
from keras.optimizers import schedules
schedules.ExponentialDecay(
        initial_learning_rate=learning_rate,decay_steps=6,staircase=True,decay_rate=0.7
    )
'''

