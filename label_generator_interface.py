from label_generator import Label
from db_login_interface import DBLoginUI
from inventory_db_connector import InventoryDBConnector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import datetime
import string
import random
import cv2

class LabelGeneratorUI(QMainWindow):
    def __init__(self):
        #initialize UI
        super(LabelGeneratorUI,self).__init__()
        #Load UI file
        uic.loadUi("UI Layouts//label.ui",self)
        #Show applicaiton
        self.show()
        self.set_ui_components()

        self.generate_product_number_button.clicked.connect(lambda: self.on_generate_product_number_clicked())
        self.generate_button.clicked.connect(lambda: self.on_generate_clicked())
        self.menu_button.clicked.connect(lambda: self.on_menu_clicked())
        self.exit_button.clicked.connect(lambda:self.on_exit_clicked())
        self.db_button.clicked.connect(lambda:self.on_db_clicked())
        self.test_button.clicked.connect(lambda:self.on_test_clicked())
        self.dst_tool_button.clicked.connect(lambda: self.on_dst_tool_clicked())

    def set_ui_components(self):
        menu_icon_path = "Resources//menu icon.png"
        menu_button_icon = QIcon(menu_icon_path)
        self.menu_button.setIcon(menu_button_icon)
        self.menu_button.setIconSize(QSize(40,40))

        exit_icon_path = "Resources//menu icon 2.png"
        exit_button_icon = QIcon(exit_icon_path)
        self.exit_button.setIcon(exit_button_icon)
        self.exit_button.setIconSize(QSize(40,40))

        db_icon_path = "Resources//db icon.png"
        db_button_icon = QIcon(db_icon_path)
        self.db_button.setIcon(db_button_icon)
        self.db_button.setIconSize(QSize(40,40))

    def on_generate_product_number_clicked(self):
        # initializing size of string
        N = 16
        product_number = ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=N))
        
        self.product_number_edit.setText(product_number)

    def on_generate_clicked(self):
        item_name = self.get_item_name()
        brand_name = self.get_brand_name()
        product_number = self.get_product_number()
        weight = self.get_weight()
        quantity = self.get_quantity()
        aisle_text = self.get_aisle_letter_and_number()
        checkout_datetime=self.get_checkout_date()
        missing_value_check = self.check_for_missing_values(item_name,brand_name,product_number,weight,quantity)
        if missing_value_check == True:
            label = Label(item_name,brand_name,aisle_text,product_number,weight,quantity,checkout_datetime)
            self.show_label_preview(label)
            label_dst = self.dst_path_edit.text()
            filename = label_dst +"//label-" + product_number + ".png"
            cv2.imwrite(filename, label.img)

            year = datetime.datetime.now().strftime("%Y")
            month = datetime.datetime.now().strftime("%m")
            day = datetime.datetime.now().strftime("%d")
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            second = datetime.datetime.now().strftime("%S")
            checkin = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second

            year = checkout_datetime.strftime("%Y")
            month = checkout_datetime.strftime("%m")
            day = checkout_datetime.strftime("%d")
            checkout = year + "-" + month + "-" + day

            query = "INSERT INTO inventory" + \
                    "(product_no,product_name,brand,weight,quantity,aisle,checkin,checkout_date)" + \
                    "VALUES ('{}','{}','{}',{},{},'{}',TO_TIMESTAMP('{}','YYYY-MM-DD HH24:MI:SS'),TO_DATE('{}','YYYY-MM-DD'))" \
                        .format(product_number,item_name,brand_name,weight,quantity,aisle_text,checkin,checkout)
            self.conn.insert_db(query)

    def on_dst_tool_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self,'Select directory')
        self.dst_path_edit.setText(dir_path)

    def on_menu_clicked(self):
        self.exit_button.show()
        self.menu_anim = QPropertyAnimation(self.menu_background, b"geometry")
        self.menu_anim.setEndValue(QRect(10,10,40,200))
        self.menu_anim.setDuration(500)
        self.menu_anim.start()

        def on_menu_clicked_part2():
            self.menu_anim2 = QPropertyAnimation(self.menu_background, b"geometry")
            self.menu_anim2.setEndValue(QRect(10,10,200,200))
            self.menu_anim2.setDuration(500)
            self.menu_anim2.start()

        self.menu_anim.finished.connect(on_menu_clicked_part2)
        self.menu_button.hide()
        self.menu_background.show()
        
    def on_exit_clicked(self):
        self.exit_anim = QPropertyAnimation(self.menu_background, b"geometry")
        self.exit_anim.setEndValue(QRect(10,10,40,200))
        self.exit_anim.setDuration(500)
        self.exit_anim.start()

        def on_exit_clicked_part2():
            self.menu_anim2 = QPropertyAnimation(self.menu_background, b"geometry")
            self.menu_anim2.setEndValue(QRect(10,10,40,40))
            self.menu_anim2.setDuration(500)
            self.menu_anim2.start()
            
        self.exit_anim.finished.connect(on_exit_clicked_part2)
        self.menu_button.show()
        self.exit_button.hide()

    def on_db_clicked(self):
        self.login_window = DBLoginUI()
        self.login_window.setWindowTitle('Database Login')
        self.login_window.main_app = self
        self.login_window.show()

    def login_to_database(self,user,password,host,port,db):
        self.conn = InventoryDBConnector()
        try:
            self.conn.connect_to_db(db,host,user,password,port)
            print("Database connection established!")
            self.login_window.hide()
        except Exception as e:
            print("Could not connect to database!")
            print(e)

    def get_item_name(self):
        return self.item_name_edit.text()

    def get_brand_name(self):
        return self.brand_name_edit.text()

    def get_product_number(self):
        return self.product_number_edit.text()

    def get_weight(self):
        return self.weight_edit.text()

    def get_quantity(self):
        return self.quantity_edit.text()

    def get_aisle_letter_and_number(self):
        aisle_letter = str(self.aisle_letter_combo.currentText())
        aisle_number = str(self.aisle_number_spin.value())
        return aisle_letter + aisle_number

    def get_checkout_date(self):
        date = self.calendar.selectedDate()
        return datetime.datetime(date.year(),date.month(),date.day())
    
    def show_label_preview(self,label):
        qimage = QImage(label.img, label.img.shape[1], label.img.shape[0],                                                                                                                                                 
                     QImage.Format_RGB888)
        pixmap = QPixmap(qimage).scaled(label.img.shape[1]*0.6, label.img.shape[0]*0.6, Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)                                                                                                                                                  
        self.label_preview.setScene(scene) 
    
    def check_for_missing_values(self,item_name,brand_name,product_number,weight,quantity):
        if len(item_name) == 0:
            message = QMessageBox()
            message.setText("Please provide the name of the item.")
            message.setWindowTitle('Error Message')
            message.exec_()
            return False
        elif len(brand_name) == 0:
            message = QMessageBox()
            message.setText("Please provide the name of the brand.")
            message.setWindowTitle('Error Message')
            message.exec_()
            return False
        elif len(product_number) == 0:
            message = QMessageBox()
            message.setText("Please provide the product number or generate one.")
            message.setWindowTitle('Error Message')
            message.exec_()
            return False
        elif len(quantity) == 0:
            message = QMessageBox()
            message.setText("Please provide the name of the brand.")
            message.setWindowTitle('Error Message')
            message.exec_()
            return False
        elif len(weight) == 0:
            message = QMessageBox()
            message.setText("Please provide the weight of the package in lbs.")
            message.setWindowTitle('Error Message')
            message.exec_()
            return False
        return True

def main():
    app = QApplication([])
    window = LabelGeneratorUI()
    window.setWindowTitle('Inventory Entry Interface')
    app.exec()
    

if __name__ == "__main__":
    main()