import cv2, os
from pathlib import Path
from threading import Thread
import tkinter as tk
from tkinter import Tk, scrolledtext, END

class input_parameter_UI(Tk):
    def __init__(self, backend, image_dir_path) -> None:
        super().__init__()
        self.backend = backend
        self.image_dir_path = image_dir_path
        self.width = 1000
        self.heigth = 550
        self.x_position = int(0.5*self.winfo_screenwidth()-0.5*self.width)
        self.y_position =  int(0.5*self.winfo_screenheight()-0.5*self.heigth)
        self.geometry(f'{str(self.width)}x{str(self.heigth)}+{str(self.x_position)}+{str(self.y_position)}')
        self.title("parameter setting")
        self.class_dict = {
            0: "Amelia Watson", 1: "Ceres Fauna", 2: "Gawr Gura", 3 : "Hakos Baelz",
            4: " IRys", 5:" Mori Calliope", 6: "Nanashi Mumei", 7: "Ninomea Ina'nis",
            8: "Ouro Kronii", 9: "Sana Tsukumo", 10: "Takanashi Kiara"
        }
        self.font = ("Times",24)
        self.text = ""

        current_row=0
        self.text_box = scrolledtext.ScrolledText(self,font=("Times",16))
        self.class_button_dict = {0:tk.Button(self,text="0")}
        for i in range(0,4):
            self.class_button_dict[i] = tk.Button(
                self,text=self.class_dict[i],font=self.font,
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
            class_name = self.class_dict[i]
            self.class_button_dict[i] = tk.Button(
                self,text=self.class_dict[i],font=self.font,
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
                self,text=self.class_dict[i],font=self.font,
                command= lambda i=i:input_parameter_UI.add_class(self,i)
            )
            self.class_button_dict[i].place(
                x=input_parameter_UI.x_abs(i-8),
                y=input_parameter_UI.y_abs(current_row),
                width=input_parameter_UI.width_abs(1),
                height=input_parameter_UI.height_abs(1)
            )
        self.start_button = tk.Button(self,text="start",font=self.font,command= self.iterate_over_dir_thread)
        self.start_button .place(
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
        for path in Path(self.image_dir_path).rglob('*.jpg'):
            self.current_image_path = os.path.join(path.parent,path.name)
            self.picture_UI = picture_UI(self)

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
        self.text = self.text_box.get("1.0", END)
        self.backend.push_to_txt_file(self.current_image_path+" <path end>"+self.text)
        self.text_box.delete("1.0","end")


class picture_UI():
    def __init__(self, mainUI:input_parameter_UI) -> None:
        self.mainUI = mainUI
        self.image_path = self.mainUI.current_image_path
        self.show_image_UI()

    def click_event(self, event, x, y , flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates on the Shell
            # print(str(x)+','+ str(y)+',')
            self.mainUI.add_coordinate(str(x)+','+ str(y)+',')
            # cv2.putText(self.img, str(x) + ',' +str(y), (x,y),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('image', self.img)

    def show_image_UI(self):
        self.img = cv2.imread(self.image_path,1)
        cv2.imshow('image', self.img)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()
