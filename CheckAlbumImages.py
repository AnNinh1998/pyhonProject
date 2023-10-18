import cv2
import face_recognition
import os
import  numpy as np
from datetime import  datetime

#bước 1: Load ảnh từ Kho ảnh nhận dạng
path= "Pictures"
images = []
className = []
myList = os.listdir(path)
#print(myList) #['check_n2.jpg', 'check_output.jpg']
for item in myList:
    curImg = cv2.imread(f"{path}/{item}") #pic2/check_n2.jpg
    images.append(curImg)
    className.append(os.path.splitext(item)[0])
    #splitext tách path thành 2 phần, phần tên và phần đuôi item
    #print(item)
#print(len(images)) xác định số lượng ảnh trong kho
print(className)

#bước 2: Mã hóa kho ảnh
def Mahoa(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return  encodeList
encodeListKnown = Mahoa(images)
print("Mã hóa thành công", len(encodeListKnown))
#Define biến tham gia để lấy kết quả ghi vào file thamgia.csv
def thamgia(name):
    with open("thamgiatest.csv","r+") as f:
        myDataList = f.readline()
        nameList=[]
        for line in myDataList:
            entry= line.split(",")
            nameList.append(entry[0])
        if name not in myDataList:
            now=datetime.now()
            datetimeString= now.strftime("%d-%m-%Y %H:%M:%S")
            f.writelines(f"\n{name},{datetimeString}")

#Khởi động webcam, camera
cam = cv2.VideoCapture(1) # sử dụng cam on runtime live máy tính
#cam = cv2.VideoCapture("test.mp4") #sử dụng video được tải lên
while True:
    ret, frame = cam.read()
    frams = cv2.resize(frame,(0,0),None,fx=0.5, fy=0.5)
    frams = cv2.cvtColor(frams,cv2.COLOR_BGR2RGB)

    #Xác định vị trí khuôn mặt và mã hóa khuôn mawjt trên cam
    faceCurrentFrame= face_recognition.face_locations(frams) # Lấy từng khuôn mặt và vị trí khuôn mặt hiện tại
    encodeFaceCurent= face_recognition.face_encodings(frams)

    for encodeFace,faceLocation in zip(encodeFaceCurent, faceCurrentFrame):
        # Lấy từng khuôn mặt và vị trí khuôn mặt hiện tại theo cam
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        result= face_recognition.compare_faces(encodeListKnown,encodeFace)
        print(result,faceDis)
        matchMin=np.argmin(faceDis)
        if faceDis[matchMin]<0.60:
            name= className[matchMin].upper()
            thamgia(name)
        else:
            name= "Unknown"
        #In tên trên frame
        y1, x2, y2, x1 = faceLocation
        y1, x2, y2, x1= y1*2, x2*2, y2*2, x1*2
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frame, name, (x2,y2), cv2.FONT_HERSHEY_COMPLEX,1, (255,255,255),2)


    cv2.imshow("Màn hình cam",frame)
    if cv2.waitKey(1) == ord("q"): # độ trễ 1/1000s, bấm q sẽ tắt
        break
