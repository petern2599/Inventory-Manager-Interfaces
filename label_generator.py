import cv2
import numpy as np
import textwrap
import qrcode
import datetime
import string
import random
 
class Label():
    def __init__(self,item_name,brand_name,aisle_text,product_number,weight,quantity,checkout):
        self.width = 400
        self.height = 600
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 0.75
        self.font_thickness = 1

        self.img = np.zeros((self.height,self.width,3), np.uint8)
        self.img.fill(255)
        cv2.rectangle(self.img,(10,10),(self.width - 10,self.height-10),(0,0,0),5)
        cv2.rectangle(self.img,(int(self.width/2)-5,int(self.img.shape[1] * (2/3)) + 180),
                      (int(self.width/2)+5,self.height-30),(0,0,0),-1)

        self.generate_qr_code(product_number)
        self.generate_item_name_text(item_name)
        self.generate_brand_name_text(brand_name)
        self.generate_checkin_text()
        self.generate_checkout_text(checkout)
        self.generate_aisle_text(aisle_text)
        self.generate_weight_text(weight)
        self.generate_quantity_text(quantity)
        self.generate_icon()

    def generate_qr_code(self,product_number):
        # Creating an instance of QRCode class
        qr = qrcode.QRCode(version = 1,
                        box_size = 14,
                        border = 1)
        
        # Adding data to the instance 'qr'
        qr.add_data(product_number)
        
        qr.make(fit = True)
        qr_img = qr.make_image(fill_color = 'black',
                            back_color = 'white').convert('RGB')
        print(qr_img.size)
        
        self.img[15:15+qr_img.size[0],15:15+qr_img.size[1]] = qr_img

    def generate_icon(self):
        path = "Resources//package-icon.png"
        icon_img = cv2.imread(path)
        self.img[30:30+icon_img.shape[0],335:335+icon_img.shape[1]] = icon_img
        cv2.putText(self.img,"Inventory Co. ",(330,70), self.font,
                        0.25, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
    
    def generate_weight_text(self,weight):
        weight_name_x = 300
        weight_name_y = int(self.img.shape[1] * (2/3)) + 80
        weight = str(weight) + " lb"
        cv2.putText(self.img,"Weight: ",(weight_name_x,weight_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        self.generate_wrapped_text(weight_name_x+8,weight_name_y+30,weight,0.75,15)

    def generate_quantity_text(self,quantity):
        quantity_name_x = 280
        quantity_name_y = int(self.img.shape[1] * (2/3)) + 140
        quantity = str(quantity) 
        cv2.putText(self.img,"Quantity: ",(quantity_name_x,quantity_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        self.generate_wrapped_text(quantity_name_x+40,quantity_name_y+30,quantity,0.75,15)

    def generate_item_name_text(self,item_name):
        item_name_x = 30
        item_name_y = int(self.img.shape[1] * (2/3)) + 80

        cv2.putText(self.img,"Item Name: ",(item_name_x,item_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        self.generate_wrapped_text(item_name_x,item_name_y+20,item_name,0.5,25)

    def generate_brand_name_text(self,brand_name):
        brand_name_x = 30
        brand_name_y = int(self.img.shape[1] * (2/3)) + 140

        cv2.putText(self.img,"Brand: ",(brand_name_x,brand_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        self.generate_wrapped_text(brand_name_x,brand_name_y+20,brand_name,0.5,25)

    def generate_checkin_text(self):
        checkin_name_x = 30
        checkin_name_y = int(self.img.shape[1] * (2/3)) + 200

        cv2.putText(self.img,"Check-In: ",(checkin_name_x,checkin_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%b")
        day = datetime.datetime.now().strftime("%d")
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        second = datetime.datetime.now().strftime("%S")

        self.checkin_datetime = month + " " + day + ", " + year + " " + hour + ":" + minute + ":" + second
        self.generate_wrapped_text(checkin_name_x,checkin_name_y+20,self.checkin_datetime,0.5,15)

    def generate_checkout_text(self,checkout_datetime):
        checkout_name_x = 30
        checkout_name_y = int(self.img.shape[1] * (2/3)) + 280

        cv2.putText(self.img,"Check-Out: ",(checkout_name_x,checkout_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)
        
        year = checkout_datetime.strftime("%Y")
        month = checkout_datetime.strftime("%b")
        day = checkout_datetime.strftime("%d")

        checkout_datetime = month + " " + day + ", " + year
        self.generate_wrapped_text(checkout_name_x,checkout_name_y+20,checkout_datetime,0.5,15)

    def generate_aisle_text(self,aisle_text):
        aisle_name_x = 220
        aisle_name_y = int(self.img.shape[1] * (2/3)) + 200

        cv2.putText(self.img,"Aisle: ",(aisle_name_x,aisle_name_y), self.font,
                        self.font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)

        cv2.putText(self.img,aisle_text,(aisle_name_x-10,aisle_name_y+100), self.font,
                        self.font_size*5, 
                        (0,0,0), 
                        self.font_thickness*5, 
                        lineType = cv2.LINE_AA)
        
    def generate_wrapped_text(self,x,y,text,font_size,width):
        wrapped_text = textwrap.wrap(text, width)
        for i, line in enumerate(wrapped_text):
            textsize = cv2.getTextSize(line, self.font, font_size, self.font_thickness)[0]

            gap = textsize[1] + 5

            y_new = y + i * gap

            cv2.putText(self.img, line, (x, y_new), self.font,
                        font_size, 
                        (0,0,0), 
                        self.font_thickness, 
                        lineType = cv2.LINE_AA)

    
if __name__=="__main__":

    item_name = "Item Name Placeholder"
    brand_name = "The Super Cool Company"
    aisle_text = "A1"
    # initializing size of string
    N = 16
    product_number = ''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=N))
    
    weight = 2.5
    quantity = 24
    checkout = datetime.datetime(2023,4,27)
    label = Label(item_name,brand_name,aisle_text,product_number,weight,quantity,checkout)

    while True:
        #Show image in window
        cv2.imshow('Label',label.img)

        #If we wait at least 1 ms and pressed the ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    #Destroys all windows
    cv2.destroyAllWindows()

