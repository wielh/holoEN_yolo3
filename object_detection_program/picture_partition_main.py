from picture_partition_backend import backend,push_none_to_txt_file

'''
backend(
    "C:\\Users\\William\\Desktop\\hololive_yolo3\\train.txt",
    "C:\\Users\\William\\Desktop\\hololive_yolo3\\object_detction_images\\"
)
'''

push_none_to_txt_file(
    "C:\\Users\\William\\Desktop\\hololive_yolo3\\train.txt",
    "C:\\Users\\William\\Desktop\\hololive_yolo3\\object_detction_images\\",
    "C:\\Users\\William\\Desktop\\hololive_yolo3\\"
)


'''
import os
text_path_1 = "C:\\Users\\William\\Desktop\\hololive_yolo3\\train.txt"
index=0
f1 = open(text_path_1,'r')
while True:
    line = f1.readline()
    index+=1
    early_stop=False
    if not line:
        break

    try:
        path, box = line.split("<path end>",maxsplit=1)
    except:
        path = line.split("<path end>",maxsplit=0)

    if not os.path.isfile(path):
        print(index)
        print(path)

f1.close()
'''

'''
f1 = open("C:\\Users\\William\\Desktop\\hololive_yolo3\\train.txt",mode="r")
f2 = open("C:\\Users\\William\\Desktop\\hololive_yolo3\\train.txt_new",mode="w")
start_dir = "C:\\Users\\William\\Desktop\\hololive_yolo3\\"

myline = f1.readline()
while myline:
    if myline.startswith(start_dir):
        myline = myline[len(start_dir):]
    f2.write(myline)
    myline = f1.readline()

f1.close()
f2.close()
'''

