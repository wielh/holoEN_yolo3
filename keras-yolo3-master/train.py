"""
Retrain the YOLO model for your own dataset.
"""
import train_model_config
import numpy as np
import keras.backend as K
import tensorflow as tf
from keras.layers import Input, Lambda
from keras.models import Model,load_model

from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
from yolo3.utils import get_random_data

def _main():
    annotation_path = train_model_config.annotation_path
    classes_path = train_model_config.classes_path
    anchors_path = train_model_config.anchors_path
    class_names = get_classes(classes_path)
    num_classes = len(class_names)
    anchors = get_anchors(anchors_path)
    input_shape = (416,416) # multiple of 32, hw
    is_tiny_version = len(anchors)==6 # default setting

    if train_model_config.retrain:
        print("=============Retrain model=============")
        if is_tiny_version:
            print("retrain tiny model")
            model = create_tiny_model(
                input_shape, anchors, num_classes, freeze_body=2,
                weights_path = train_model_config.log_dir + train_model_config.load_weight_name)
        else:
            model = create_model(
                input_shape, anchors, num_classes, freeze_body=2,
                weights_path= train_model_config.log_dir + train_model_config.load_weight_name)
                # make sure you know what you freeze
    else:
        print("=============Create model=============")
        if is_tiny_version:
            print("create tiny model")
            model = create_tiny_model(
                input_shape, anchors, num_classes,freeze_body=2, load_pretrained= False)
        else:
            model = create_model(
                input_shape, anchors, num_classes,freeze_body=2, load_pretrained= False)
            # make sure you know what you freeze

    with open(annotation_path) as f:
        lines = f.readlines()
    np.random.seed(train_model_config.seed)
    np.random.shuffle(lines)
    np.random.seed(None)
    num_val = int(len(lines)*train_model_config.val_split)
    num_train = len(lines) - num_val

    # not to unfreeze all layers
    # unfreeze and train by the following order
    # (160, 219)(220,max)
    if True:
        yololoss = lambda y_true, y_pred: y_pred
        print("total layers:",len(model.layers))
        opt = train_model_config.get_optimizer()
        batch_size = train_model_config.batch_size
        print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))

        '''
        for i in range(len(model.layers)):
                model.layers[i].trainable = False

        for i in range(230):
            if not model.layers[i].name.startswith("conv2d"):
                model.layers[i].trainable = True
        '''
        for i in range(len(model.layers)):
            model.layers[i].trainable = True
        for i in range(len(model.layers)):
            if  model.layers[i].trainable:
                print("layer ",i,",", model.layers[i].name ," is trainable")
        model.compile(optimizer = opt, loss={'yolo_loss': yololoss})
        model.summary()
        model.fit(
            data_generator_wrapper(
                lines[:num_train], batch_size, input_shape, anchors, num_classes,True),
            steps_per_epoch=max(1, num_train//batch_size),
            validation_data=data_generator_wrapper(
                lines[num_train:], batch_size, input_shape, anchors, num_classes,False),
            validation_steps=max(1, num_val//batch_size),
            epochs = train_model_config.epochs,
            callbacks = train_model_config.callbacks,
        )
        for i in range(len(model.layers)):
            model.layers[i].trainable = False
        model.save_weights(train_model_config.log_dir + train_model_config.save_weight_name)

    '''
    # Unfreeze and continue training, to fine-tune.
    # Train longer if the result is not good.
    if True:
        for i in range(len(model.layers)):
            model.layers[i].trainable = True
        model.compile(optimizer = train_model_config.get_optimizer(1e-3),
        loss={'yolo_loss': lambda y_true, y_pred: y_pred}) # recompile to apply the change
        print('Unfreeze all of the layers.')

        batch_size = train_model_config.batch_size # note that more GPU memory is required after unfreezing the body
        print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
        model.fit_generator(
            data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes),
            steps_per_epoch=max(1, num_train//batch_size),
            validation_data=data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors, num_classes),
            validation_steps=max(1, num_val//batch_size),
            epochs=train_model_config.epochs,
            initial_epoch=3,
            callbacks=train_model_config.callbacks)
        model.save(train_model_config.log_dir + train_model_config.save_model_name)
    '''

def get_classes(classes_path):
    '''loads the classes'''
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names

def get_anchors(anchors_path):
    '''loads the anchors from a file'''
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)

def create_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
            weights_path='model_data/yolo_weights.h5'):
    '''create the training model'''
    print("This is a big model")
    K.clear_session() # get a new session
    image_input = Input(shape=(None, None, 3))
    h, w = input_shape
    num_anchors = len(anchors)

    y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], \
        num_anchors//3, num_classes+5)) for l in range(3)]

    model_body = yolo_body(image_input, num_anchors//3, num_classes)
    print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

    if load_pretrained:
        model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
        print('Load weights {}.'.format(weights_path))
        if freeze_body in [1, 2]:
            # Freeze darknet53 body or freeze all but 3 output layers.
            num = (185, len(model_body.layers)-3)[freeze_body-1]
            for i in range(num): model_body.layers[i].trainable = False
            print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
        arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
        [*model_body.output, *y_true])
    model = Model([model_body.input, *y_true], model_loss)

    return model

def create_tiny_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
            weights_path='model_data/tiny_yolo_weights.h5'):
    '''create the training model, for Tiny YOLOv3'''
    print("This is a tiny model")
    K.clear_session() # get a new session
    image_input = Input(shape=(None, None, 3))
    h, w = input_shape
    num_anchors = len(anchors)

    y_true = [Input(shape=(h//{0:32, 1:16}[l], w//{0:32, 1:16}[l], \
        num_anchors//2, num_classes+5)) for l in range(2)]

    model_body = tiny_yolo_body(image_input, num_anchors//2, num_classes)
    print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

    if load_pretrained:
        model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
        print('Load weights {}.'.format(weights_path))
        if freeze_body in [1, 2]:
            # Freeze the darknet body or freeze all but 2 output layers.
            num = (20, len(model_body.layers)-2)[freeze_body-1]
            for i in range(num): model_body.layers[i].trainable = False
            print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
        arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})(
        [*model_body.output, *y_true])
    model = Model([model_body.input, *y_true], model_loss)

    return model

def data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes, random=True):
    '''data generator for fit_generator'''
    n = len(annotation_lines)
    i = 0
    while True:
        image_data = []
        box_data = []
        for b in range(batch_size):
            if i==0:
                np.random.shuffle(annotation_lines)
            image, box = get_random_data(annotation_lines[i], input_shape, random=random)
            image_data.append(image)
            box_data.append(box)
            i = (i+1) % n
        image_data = np.array(image_data)
        box_data = np.array(box_data)
        y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
        yield [image_data, *y_true], np.zeros(batch_size)

def data_generator_wrapper(annotation_lines, batch_size, input_shape, anchors, num_classes, random=True):
    n = len(annotation_lines)
    if n==0 or batch_size<=0: return None
    return data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes, random)

if __name__ == '__main__':
    _main()
