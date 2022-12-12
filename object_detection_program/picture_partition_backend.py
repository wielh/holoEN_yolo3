import os
from threading import Thread
from picture_partition_UI import input_parameter_UI,picture_UI
from pathlib import Path


def push_none_to_txt_file(text_path:str, image_dir_path:str, root:str):
    f = open(text_path,'a')
    for path in Path(image_dir_path).rglob('*.jpg'):
        path = os.path.join(path.parent,path.name)
        if path.startswith(root):
            path = path[len(root):]
        f.write(path+"<path end>\n")
    f.close()

class backend():
    def __init__(self, text_path, image_dir_path, root) -> None:
        self.text_path = text_path
        self.image_dir_path = image_dir_path
        self.root = root
        self.mainUI = input_parameter_UI(self,image_dir_path=image_dir_path)

    def iterate_over_dir(self):
        for path in Path(self.image_dir_path).rglob('*.jpg'):
            self.picture_UI = picture_UI(self, os.path.join(path.parent,path.name))

    def push_to_txt_file(self, text:str):
        f = open(self.text_path,'a')
        content = text.replace("\n"," ")+"\n"
        if content.startswith(self.root):
            content = content[len(self.root):]
        f.write()
        f.close()

    def start():
        pass


