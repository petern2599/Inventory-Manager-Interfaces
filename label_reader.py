import cv2

def draw_detection_box(values,points,img):
    for label_count in range(len(values)):
        cv2.rectangle(img,(int(points[label_count][0][0]),int(points[label_count][0][1])),
                    (int(points[label_count][2][0]),int(points[label_count][2][1])),(255,0,0),3)
        
        cv2.rectangle(img,(int(points[label_count][0][0]),int(points[label_count][0][1])-20),
                    (int(points[label_count][2][0] - (points[label_count][2][0] - points[label_count][0][0])*0.1),
                    int(points[label_count][0][1])),(255,0,0),-1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 0.3
        font_thickness = 1
        cv2.putText(img,values[label_count],(int(points[label_count][0][0]),int(points[label_count][0][1])-5), 
                        font,
                        font_size, 
                        (255,255,255), 
                        font_thickness, 
                        lineType = cv2.LINE_AA)
    return img

capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
while True:
    #When capturing video, its just a series of image framesqq
    ret,frame = capture.read()

    det_ret, values, points, straight_qrcodes = detector.detectAndDecodeMulti(frame)
    frame = draw_detection_box(values,points,frame)
    #Show image in window
    cv2.imshow('Label',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Destroys all windows
cv2.destroyAllWindows()
capture.release()
