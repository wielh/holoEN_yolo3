import cv2

class picture_UI():
    def __init__(self, mainUI, current_image_path) -> None:
        self.mainUI = mainUI
        self.image_path = current_image_path
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

