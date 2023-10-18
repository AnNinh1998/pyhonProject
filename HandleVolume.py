import cv2
import time
import hand as htm
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime=0
#Khởi động camera
cam=cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=int(0.7))#Độ tin cậy bằng 0.7
#Thư viện Pycaw handle Volume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange= volume.GetVolumeRange()#Phạm vi âm lượng, min=-65,25 max=0
minVol= volRange[0]
maxVol= volRange[1]

while True:
    ret, frame= cam.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    #print(lmList)#Laasy tọa độ các điểm ngosn tay

    if len(lmList)!=0:
        #print(lmList[4],lmList[8])#Lấy tọa độ ngón cái và ngón trỏ
        #Lấy tọa độ (x1,y1) của ngón cái, (x2,y2) của ngón trỏ
        x1,y1= lmList[4][1],lmList[4][2]
        x2,y2= lmList[8][1],lmList[8][2]

        #Vẽ hình tròn tại 2 đầu ngón cái và ngón trỏ
        cv2.circle(frame,(x1,y1),10,(255,0,255),2)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), 2)
        #vẽ đường thẳng nối ngón cái và ngón trỏ
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)
        #xác định trung điểm của đường thẳng nối 2 ngón tay
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(frame, (cx, cy), 10, (255,0,255), -1)

        #Tính độ dài đoạn thẳng nối 2 ngón tay
        length= math.hypot(x2-x1,y2-y1)
        #print(length)
        #Dải âm thanh trên máy
        vol= np.interp(length,[25,230],[minVol,maxVol])
        volBar= np.interp(length,[25,230],[400,150])
        vol_Tyle= np.interp(length,[25,230],[0,100])
        print(length,vol)
        #interp chuyển độ dài ngón tay trong khoảng (25,230) nawfm trong khoảng minVol, maxVol
        volume.SetMasterVolumeLevel(vol, None)
        if length<20:
            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
        #Vẽ hình chủ nhật thể hiện % pin
        cv2.rectangle(frame, (50, 150), (30, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volBar)), (30, 400), (0, 255, 0), -1)
        #show % pin trên khối hình chữ nhật
        cv2.putText(frame, f"{int(vol_Tyle)} %", (40,70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    #show fps
    cTime = time.time()  # trả về số giây, tính theo giờ utc, gọi là thời điểm bắt đầu thời gian
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS:{int(fps)}", (150, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 128), 3)
    #show màn hình
    cv2.imshow("Màn hình cam", frame)
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s, bấm q sẽ tắt
        break
cam.release()
cv2.destroyWindow()