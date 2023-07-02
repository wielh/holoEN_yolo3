from pathlib import Path
from threading import Thread
import os, shutil

import tkinter as tk
from tkinter import Tk, scrolledtext, END
from data_fetch.show_picture_UI import picture_UI

class input_parameter_UI(Tk):
    class_dict = {
        0: "Amelia Watson", 1: "Ceres Fauna", 2: "Gawr Gura", 3 : "Hakos Baelz",
        4: " IRys", 5:" Mori Calliope", 6: "Nanashi Mumei", 7: "Ninomea Ina'nis",
        8: "Ouro Kronii", 9: "Sana Tsukumo", 10: "Takanashi Kiara"
    }

    def __init__(self) -> None:
        super().__init__()
        self.width = 1000
        self.heigth = 700
        self.x_position = int(0.5*self.winfo_screenwidth()-0.5*self.width)
        self.y_position =  int(0.5*self.winfo_screenheight()-0.5*self.heigth)
        self.geometry(f'{str(self.width)}x{str(self.heigth)}+{str(self.x_position)}+{str(self.y_position)}')
        self.title("parameter setting")
        self.font = ("Times",24)
        self.text = ""
        current_row=0

        self.train_image_input_label = tk.Label(self, text='images_path', font=self.font)
        self.train_image_input_label.place(
            x=input_parameter_UI.x_abs(0),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(2),
            height=input_parameter_UI.height_abs(1)
        )
        self.train_image_input_text = tk.Text(self, font=self.font)
        self.train_image_input_text.place(
            x=input_parameter_UI.x_abs(2),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(4),
            height=input_parameter_UI.height_abs(1)
        )
        current_row+=1

        self.train_image_output_label = tk.Label(self, text='images_after_record_path', font=self.font)
        self.train_image_output_label.place(
            x=input_parameter_UI.x_abs(0),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(2),
            height=input_parameter_UI.height_abs(1)
        )
        self.train_image_output_text = tk.Text(self, font=self.font)
        self.train_image_output_text.place(
            x=input_parameter_UI.x_abs(2),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(4),
            height=input_parameter_UI.height_abs(1)
        )
        current_row+=1

        self.data_record_textfile_path_label = tk.Label(self, text='data_record_file', font=self.font)
        self.data_record_textfile_path_label.place(
            x=input_parameter_UI.x_abs(0),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(2),
            height=input_parameter_UI.height_abs(1)
        )
        self.data_record_textfile_path_text = tk.Text(self, font=self.font)
        self.data_record_textfile_path_text.place(
            x=input_parameter_UI.x_abs(2),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(4),
            height=input_parameter_UI.height_abs(1)
        )
        current_row+=1

        self.class_button_dict = {}
        for i in range(0,4):
            self.class_button_dict[i] = tk.Button(
                self,
                text = input_parameter_UI.class_dict[i],
                font=self.font,
                command=lambda i=i:input_parameter_UI.add_class(self,i)
            )
            self.class_button_dict[i].place(
                x=input_parameter_UI.x_abs(i),
                y=input_parameter_UI.y_abs(current_row),
                width=input_parameter_UI.width_abs(1),
                height=input_parameter_UI.height_abs(1)
            )
        current_row+=1
        for i in range(4,8):
            self.class_button_dict[i] = tk.Button(
                self,
                text=input_parameter_UI.class_dict[i],
                font=self.font,
                command=lambda i=i:input_parameter_UI.add_class(self,i)
            )
            self.class_button_dict[i].place(
                x=input_parameter_UI.x_abs(i-4),
                y=input_parameter_UI.y_abs(current_row),
                width=input_parameter_UI.width_abs(1),
                height=input_parameter_UI.height_abs(1)
            )
        current_row+=1
        for i in range(8,11):
            self.class_button_dict[i] = tk.Button(
                self,
                text=input_parameter_UI.class_dict[i],
                font=self.font,
                command= lambda i=i:input_parameter_UI.add_class(self,i)
            )
            self.class_button_dict[i].place(
                x=input_parameter_UI.x_abs(i-8),
                y=input_parameter_UI.y_abs(current_row),
                width=input_parameter_UI.width_abs(1),
                height=input_parameter_UI.height_abs(1)
            )
        self.start_button = tk.Button(self,text="start",font=self.font,command= self.iterate_over_dir_thread)
        self.start_button.place(
            x=input_parameter_UI.x_abs(3),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(1),
            height=input_parameter_UI.height_abs(1)
        )

        current_row+=2
        self.clear_button =tk.Button(
            self,text="clear",font=self.font,command=self.clear
        )
        self.clear_button.place(
            x=input_parameter_UI.x_abs(0),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(2),
            height=input_parameter_UI.height_abs(1)
        )
        self.submit_button =tk.Button(
            self,text="submit",font=self.font,command=self.submit
        )
        self.submit_button.place(
            x=input_parameter_UI.x_abs(2),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(2),
            height=input_parameter_UI.height_abs(1)
        )
        current_row+=1

        self.text_box = scrolledtext.ScrolledText(self,font=("Times",16))
        self.text_box.place(
            x= input_parameter_UI.x_abs(0),
            y=input_parameter_UI.y_abs(current_row),
            width=input_parameter_UI.width_abs(4),
            height= input_parameter_UI.height_abs(6),
        )
        current_row+=6

        self.protocol('WM_DELETE_WINDOW', self.destroy_both_frame)
        self.mainloop()

    def destroy_both_frame(self):
        self.destroy()

    def iterate_over_dir_thread(self):
        self.image_thread = Thread(target = self.iterate_over_dir)
        self.image_thread.setDaemon(True)
        self.image_thread.start()

    def iterate_over_dir(self):
        images_root_path = self.train_image_input_text.get("1.0",END).replace("\n","")
        images_output_root_path = self.train_image_output_text.get("1.0",END).replace("\n","")

        for path in Path(images_root_path).rglob('*.jpg'):
            image_src = os.path.join(path.parent,path.name)
            relative_path = os.path.relpath(image_src, images_root_path)
            self.current_image_path = os.path.join(images_output_root_path,relative_path)
            self.picture_UI = picture_UI(self, image_src)
            if not os.path.exists(os.path.dirname(self.current_image_path)):
                os.makedirs(os.path.dirname(self.current_image_path))
            shutil.move(image_src, self.current_image_path)

    #=========================================================================
    grid_width=250
    grid_height=50

    def x_abs(x:int)->int:
        return x*input_parameter_UI.grid_width+5

    def y_abs(y:int)->int:
        return y*input_parameter_UI.grid_height+2

    def width_abs(width:int) ->int:
        return width*input_parameter_UI.grid_width-10

    def height_abs(height:int) ->int:
        return height*input_parameter_UI.grid_height-4
    #=========================================================================

    def add_coordinate(self,coordinates:str):
        self.text_box.insert(END,coordinates)

    def add_class(self,class_num):
        self.text_box.insert(END,str(class_num)+"\n")

    def clear(self):
        self.text_box.delete("1.0","end")

    def submit(self):
        text = self.current_image_path + "<PathEnd>"
        text += self.text_box.get("1.0", END).replace("\n"," ")
        text += "\n"
        text_path = self.data_record_textfile_path_text.get("1.0", END).replace("\n","")
        f = open(text_path,'a')
        f.write(text)
        f.close()
        self.text_box.delete("1.0", END)



