from tensorflow.keras.optimizers import SGD,Adagrad,Adam
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import schedules
from sklearn.metrics import confusion_matrix

retrain = True
annotation_path = 'train.txt'
log_dir = 'object_detection_models/logs/001/'
load_weight_name = 'new_weight_8.h5'
save_weight_name = 'new_weight_9.h5'
classes_path = 'keras-yolo3-master/model_data/voc_classes.txt'
anchors_path = 'keras-yolo3-master/model_data/yolo_anchors.txt'

save_tiny_weight_path = "object_detection_models/logs/000/new_weight_1.h5"
default_save_weight_path = 'keras-yolo3-master/model_data/yolo_weights.h5'
default_save_tiny_weight_path = 'keras-yolo3-master/model_data/tiny_yolo_weights.h5'

logging = TensorBoard(log_dir=log_dir)
checkpoint = ModelCheckpoint(log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
    monitor='val_loss', save_weights_only=True, save_best_only=True, period=3)
early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=30, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3, verbose=1)
callbacks=[logging, checkpoint, reduce_lr]

seed = 69420
val_split = 0.1
epochs = 20
batch_size = 8
def get_optimizer(learning_rate= 1e-5):
    return SGD(learning_rate = learning_rate)

'''
schedules.ExponentialDecay(
        initial_learning_rate=learning_rate,decay_steps=6,staircase=True,decay_rate=0.7
    )
'''

