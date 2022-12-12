# holoEN_yolo3
Use yolo3 to detect hololiveEN characters in pictures

How to use the program:

   (1). Download some images by yourself
   
   (2). Execute object_detection_program/picture_partion_main.py to select object from image
        detail of selecting images: https://github.com/qqwweee/keras-yolo3
        we use the keras implementation of yolo3 on the program.
        
   (3). After selecting object from images, we edit train.txt, voc_classes.txt in
    keras-yolo3-master/model_data/
    
   (4). edit config file train_model_config.py or some setting in train.py in folderkeras-yolo3-master/.
   
   (5). build a python enviroment with requirments.txt by pip or conda
   
   (6). open terminal and cd to holoEN_yolo3.
   
   (7). train command: 
   
    python keras-yolo3-master\train.py
   
   (8). detect command: 
   
    python keras-yolo3-master\yolo_video.py --image --anchors_path {path} 
        --classes_path {path} --model_path {path}

