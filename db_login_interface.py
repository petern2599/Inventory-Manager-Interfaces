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
        self.main_app = None
        self.login_button.clicked.connect(lambda:self.on_login_clicked())
    
    def set_ui_components(self):
        path = "Resources//package-icon.png"
        qimage = QImage(path)
        pixmap = QPixmap(qimage)
        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)                                                                                                                                                  
        self.logo_view.setScene(scene)

    def on_login_clicked(self):
        user = self.user_edit.text()
        password = self.password_edit.text()
        host = self.host_edit.text()
        port = self.port_edit.text()
        db = self.db_edit.text()
        self.main_app.login_to_database(user,password,host,port,db)

def main():
    app = QApplication([])
    window = DBLoginUI()
    window.setWindowTitle('Database Login')
    app.exec()
    

if __name__ == "__main__":
    main()