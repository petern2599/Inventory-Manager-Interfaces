from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
import datetime
from pyzbar.pyzbar import decode
import numpy as np 

class CheckoutUI(QMainWindow):
    def __init__(self,app):
        #initialize UI
        super(CheckoutUI,self).__init__()
        self.main_app = app
        #Load UI file
        uic.loadUi("UI Layouts//checkout.ui",self)
        #Show applicaiton
        self.show()
        
        self.camera_button.clicked.connect(lambda: self.show_camera())
        self.checkout_button.clicked.connect(lambda: self.checkout_product_no())

        self.capture = cv2.VideoCapture(0)
        self.camera_status_label.setText("Ready")
        self.camera_status_label.setStyleSheet("background-color: lightgreen")
        

    def __del__(self):
        cv2.destroyAllWindows()
        self.capture.release()

    def draw_detection_box(self,img):
        
        cv2.polylines(img,[self.detection_points],True,(255,0,0),4)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 0.6
        font_thickness = 2
        
        x_points = []
        y_points = []
        for i in range(4):
            x_points.append(self.detection_points[i][0])
            y_points.append(self.detection_points[i][1])

        x_min = min(x_points)
        x_max = max(x_points)
        y_min = min(y_points)
        y_max = max(y_points)

        pos_x = x_max - int((x_max-x_min)*0.90)
        pos_y = y_max - int((y_max-y_min)/2)

        cv2.putText(img,self.detected_label,(pos_x,pos_y),
                    font,
                    font_size,
                    (0,0,255),
                    font_thickness,
                    lineType=cv2.LINE_AA)

        return img

    def show_camera(self):
        ret,frame = self.capture.read()
        result = decode(frame)
        if len(result) != 0:
            self.detected_label = result[0].data.decode('utf-8')
            self.detection_points = np.array(result[0].polygon,np.int32)
            frame = self.draw_detection_box(frame)
            self.show_product_no()
            query_result = self.main_app.conn.check_if_product_no_exists(self.detected_label)
            if query_result != None:
                expected_checkout_date = self.main_app.conn.get_expected_checkout_date_from_db(self.detected_label)
                self.expected_checkout_date_label.setText(expected_checkout_date[0])

        qimage = QImage(frame, frame.shape[1], frame.shape[0],                                                                                                                                                 
                    QImage.Format_BGR888)
        pixmap = QPixmap(qimage).scaled(frame.shape[1]*0.5, frame.shape[0]*0.5, Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)                                                                                                                                                  
        self.camera_view.setScene(scene)
        
    def show_product_no(self):
        self.product_no_label.setText(self.detected_label)

    def checkout_product_no(self):
        product_no = self.product_no_label.text()
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        second = datetime.datetime.now().strftime("%S")
        checkout = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second

        result = self.main_app.conn.check_checkout_is_null(product_no)
        if result == None:
            self.main_app.conn.submit_checkout_to_db(checkout,product_no)
        else:
            message = QMessageBox()
            message.setText("Product has already been checked out!")
            message.setWindowTitle('Error Message')
            message.exec_()

def main():
    app = QApplication([])
    window = CheckoutUI(None)
    window.setWindowTitle('Checkout Interface')
    app.exec()
    

if __name__ == "__main__":
    main()