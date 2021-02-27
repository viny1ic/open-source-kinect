import cv2
import mediapipe as mp
import pyautogui
import math

print(cv2.__version__)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def control_volume(angle, dist):
  if(40<angle<140 and dist>80):
    pyautogui.press('volumeup')
  if(-140<angle<-40 and dist>80):
    pyautogui.press('volumedown')

def move_cursor(coord):
  pyautogui.moveTo(coord[0]*1920/640, coord[1]*1080/480)

def mouse_buttons(isUp):
  if(isUp[1] and isUp[2] and isUp[3] and isUp[4]):
    pyautogui.scroll(int(((angle+1)/abs(angle+1))*dist/2))
    return
  if(isUp[2]):
    pyautogui.click()
    return
  if(isUp[3]):
    pyautogui.click(button='right')

# For webcam input:
hands = mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
first_iter = True
while cap.isOpened():
  success, image = cap.read()
  if not success:
    break
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)

  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      fingers = []
      isUp=[False,False,False,False,False]
      fingers.append((int((hand_landmarks.landmark[4].x)*640), int((hand_landmarks.landmark[4].y)*480)))
      fingers.append((int((hand_landmarks.landmark[8].x)*640), int((hand_landmarks.landmark[8].y)*480)))
      fingers.append((int((hand_landmarks.landmark[12].x)*640), int((hand_landmarks.landmark[12].y)*480)))
      fingers.append((int((hand_landmarks.landmark[16].x)*640), int((hand_landmarks.landmark[16].y)*480)))
      fingers.append((int((hand_landmarks.landmark[20].x)*640), int((hand_landmarks.landmark[20].y)*480)))
      index_begin = (int((hand_landmarks.landmark[5].x)*640), int((hand_landmarks.landmark[5].y)*480))
      little_begin = (int((hand_landmarks.landmark[17].x)*640), int((hand_landmarks.landmark[17].y)*480))
      for i in range(5):
        if fingers[i][1]<index_begin[1]:
          image = cv2.circle(image, fingers[i], 3, (0,0,255), -1)
          isUp[i]=True
      image = cv2.line(image, index_begin, little_begin, (0,255,0), 3)
      
      if(first_iter): # set reference point
        print("first iter")
        reference = fingers[1]
        first_iter=False
      image = cv2.circle(image, reference, 3, (0,255,0), -1)
      
      # calculate distance and angle of index finger from reference
      offset=[0,0]
      offset[0]=reference[0]-fingers[1][0]
      offset[1]=reference[1]-fingers[1][1]
      angle = (math.atan2(offset[1],offset[0]))*180/math.pi
      dist = math.hypot(offset[0],offset[1])
      print(angle, " ", dist)
      move_cursor(fingers[1])
      mouse_buttons(isUp)
  cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
hands.close()
cap.release()

#0 = wrist,2 = thumb base,4 = thumb tip,8 = index_tip, 12 = mid_finger_tip
#16 = 4th finger tip, 20 = little_finger_tip
