import cv2
import pytesseract
#Đường dẫn thư mục tesseract.exe
pytesseract.pytesseract.tesseract_cmd= "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img= cv2.imread("1.5.png")
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
text= pytesseract.image_to_string(img,lang="vie")
print(text)
with open("converImage2Text.txt","a",encoding="utf-8") as f:
    f.writelines(text)
