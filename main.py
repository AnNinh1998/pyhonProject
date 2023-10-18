import cv2
import face_recognition

#Load ảnh input để test

imgInput = face_recognition.load_image_file("Pictures/check_n2.jpg")
imgInput = cv2.cvtColor(imgInput,cv2.COLOR_BGR2RGB)
# Thay đổi kích thước ảnh theo tỉ lệ mới
width = 10
height = 10
resized_img = cv2.resize(imgInput, (width, height))
#Load ảnh check để test
imgCheck = face_recognition.load_image_file("Pictures/check_output.jpg")
imgCheck = cv2.cvtColor(imgCheck,cv2.COLOR_BGR2RGB)

#Xác định vị trí khuôn mặt dữ liệu vào
faceLoc = face_recognition.face_locations(imgInput)[0]
print(faceLoc) #tọa độ ảnh (y1 x2 y2 x1)
#Xác định vị trí khuôn mặt dũ liệu kiểm tra
faceLocCheck = face_recognition.face_locations(imgCheck)[0]
#Mã hóa hình ảnh Input
encodeInput = face_recognition.face_encodings(imgInput)[0]
cv2.rectangle(imgInput,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#Mã hóa hình ảnh check
encodeCheck = face_recognition.face_encodings(imgCheck)[0]
cv2.rectangle(imgCheck,(faceLocCheck[3],faceLocCheck[0]),(faceLocCheck[1],faceLocCheck[2]),(255,0,255),2)

#So sánh kết quả xác thực hình ảnh
result = face_recognition.compare_faces([encodeInput],encodeCheck)
#Sai số kết quả nhận diện khuôn mặt
faceDis = face_recognition.face_distance([encodeInput],encodeCheck)
print(result,faceDis)
# Hiển thị kết quả vẽ tọa độ
cv2.imshow("Ninhinput",imgInput)
cv2.imshow("Ninh",imgCheck)
cv2.waitKey(0)