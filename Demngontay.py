import cv2
import time
import os
import hand as htm

pTime=0
#Khởi động camera
cam= cv2.VideoCapture(0)

folderPath= "Fingers"
lst=os.listdir(folderPath)
lst_image=[]
for i in lst:
    image= cv2.imread(f"{folderPath}/{i}") #return result Fingers/1.png
    lst_image.append(image)
#print(lst_image[0].shape)
detector = htm.handDetector(detectionCon=int(0.55))
fingerID=[4,8,12,16,20]
while True:
    ret, frame = cam.read()


    frame=detector.findHands(frame)
    lmList= detector.findPosition(frame,draw=False)
    print(lmList)

    if len(lmList)!=0:
        fingerS=[]
        #Viết cho ngón cái
        if lmList[fingerID[0]][1] < lmList[fingerID[0] - 1][1]:#so sánh điểm 4 nằm bên trái hay bên phải điểm 3
            fingerS.append(1)  # nếu ngón tay đang mở append =1
        else:
            fingerS.append(0)  # nếu ngón tay đang gập sang append =0
        # viết cho ngón dài
        for id in range(1,5):
            if lmList[fingerID[id]][2] < lmList[fingerID[id]-2][2]:
                fingerS.append(1)#nếu ngón tay đang mở append =1
            else:
                fingerS.append(0)#nếu ngón tay đang gập xuống append =0
        #print(fingerS)
        songontay= fingerS.count(1)

        h, w, c = lst_image[songontay-1].shape
        frame[0:h, 0:w] = lst_image[songontay-1]
        # Vẽ hifnh chữ nhật đếm số ngón tay
        cv2.rectangle(frame, (0, 250), (100, 400), (255, 255, 0), -1)
        cv2.putText(frame, str(songontay), (10, 400), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 1)

    #Show FPS
    cTime=time.time() #trả về số giây, tính theo giờ utc, gọi là thời điểm bắt đầu thời gian
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,f"FPS:{int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,2,(0,0,128),3)


    cv2.imshow("Dem ngon tay",frame)
    if cv2.waitKey(1) == ord("q"): # độ trễ 1/1000s, bấm q sẽ tắt
        break