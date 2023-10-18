import math
import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
#Chèn ảnh vô lăng
def overlay_images(background_img, overlay_img, offset_x=0, offset_y=0):
    # Get the dimensions of the background image
    background_height, background_width = background_img.shape[0], background_img.shape[1]

    # Calculate the offset for overlaying the images
    overlay_height, overlay_width = overlay_img.shape[0], overlay_img.shape[1]
    start_x = max(0, offset_x)
    start_y = max(0, offset_y)
    end_x = min(background_width, offset_x + overlay_width)
    end_y = min(background_height, offset_y + overlay_height)

    # Crop the overlay image if it extends beyond the background boundaries
    crop_overlay = overlay_img[(start_y - offset_y):(end_y - offset_y), (start_x - offset_x):(end_x - offset_x)]

    # Create a temporary copy of the background image
    result_img = np.copy(background_img)

    # Combine the background and overlay images
    result_img[start_y:end_y, start_x:end_x] = crop_overlay

    return result_img
wheel_image=cv2.imread("volang.png")
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height, width, _ = image.shape
    if results.multi_hand_landmarks:
      hand_center=[]
      for hand_landmarks in results.multi_hand_landmarks:
        hand_center.append(
            [int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].x*height)]
        )
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        if len(hand_center)==2:
            center_x= (hand_center[0][0]+hand_center[0][1])//2
            center_y= (hand_center[1][0]+hand_center[1][1])//2
            radius= int(math.sqrt((hand_center[0][0]-hand_center[1][0])**2)
                    +(hand_center[0][1]-hand_center[1][1]**2)/2)
            #overlay_images(image, cv2.resize(wheel_image,(2*radius, 2*radius)), center_x-radius,center_y-radius)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s, bấm q sẽ tắt
        break
cap.release()
cv2.destroyWindow()