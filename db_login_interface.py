from inventory_db_connector import InventoryDBConnector

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

class DBLoginUI(QMainWindow):
    def __init__(self):
        #initialize UI
        super(DBLoginUI,self).__init__()
        #Load UI file
        uic.loadUi("UI Layouts//db_login.ui",self)
        #Show applicaiton
        self.show()
    
    def set_ui_components(self):
        path = "Resources//package-icon.png"
        qimage = QImage(path)
        pixmap = QPixmap(qimage)
        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)                                                                                                                                                  
        self.logo_view.setScene(scene)

def main():
    app = QApplication([])
    window = DBLoginUI()
    window.setWindowTitle('Database Login')
    app.exec()
    

if __name__ == "__main__":
    main()