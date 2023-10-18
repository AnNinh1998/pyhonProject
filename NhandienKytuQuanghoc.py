import cv2
import pytesseract

#Đường dẫn thư mục tesseract.exe
pytesseract.pytesseract.tesseract_cmd= "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img= cv2.imread("1.2.jpg")
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
boxes=pytesseract.image_to_data(img)
#print(boxes)
for x, b in enumerate(boxes.splitlines()):
    if x!=0:
        b=b.split()
        if len(b)==12:
            print(b)
            x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,y+h),(0, 255, 0), 3)
            cv2.putText(img,b[11],(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,0),1)

cv2.imshow("OCR",img)
cv2.waitKey()
