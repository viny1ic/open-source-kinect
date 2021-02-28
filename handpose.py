import cv2
import mediapipe as mp
import pyautogui
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

mode = int(input('Press 0 for mouse mode\nPress 1 for gesture mdoe\nPress 2 for tetris mode'))

def gesture(angle, dist, isUp):
  if(isUp[1] and isUp[2] and isUp[3]):
    if((165<angle<180 or -165<angle<-140) and dist>80):
      pyautogui.keyDown('ctrlleft')
      pyautogui.press('tab')
      pyautogui.keyUp('ctrlleft')
      time.sleep(0.1)
      return
    if((0<angle<15 or -15<angle<0) and dist>80):
      pyautogui.keyDown('ctrlleft')
      pyautogui.keyDown('shiftleft')
      pyautogui.press('tab')
      pyautogui.keyUp('shiftleft')
      pyautogui.keyUp('ctrlleft')
      time.sleep(0.1)
      return
  
  elif(isUp[1] and isUp[2]):
    if((165<angle<180 or -180<angle<-165) and dist>80):
      pyautogui.keyDown('altleft')
      pyautogui.press('tab')
      pyautogui.keyUp('altleft')
      time.sleep(0.1)
      return
    if((0<angle<15 or -15<angle<0) and dist>80):
      pyautogui.keyDown('altleft')
      pyautogui.keyDown('shiftleft')
      pyautogui.press('tab')
      pyautogui.keyUp('altleft')
      pyautogui.keyUp('shiftleft')
      time.sleep(0.1)
      return  

  elif(isUp[1]):
    if(40<angle<140 and dist>80):
      pyautogui.press('volumeup')
    if(-140<angle<-40 and dist>80):
      pyautogui.press('volumedown')


def mouse_buttons(isUp):
  if(isUp[1] and isUp[2] and isUp[3] and isUp[4]):
    pyautogui.scroll(int(((angle+1)/abs(angle+1))*dist/2))
    return
  if(isUp[2]):
    pyautogui.click()
    return
  if(isUp[3]):
    pyautogui.click(button='right')

def tetris(isUp):
  if(isUp[1] and isUp[2] and isUp[3] and isUp[4] and isUp[0]):
    return
  if(isUp[1]):
    if(isUp[2] and isUp[3] and isUp[4]):
      pyautogui.press('up')
      return
    if(isUp[2] and isUp[3]):
      pyautogui.press('down')
    if(isUp[2]):
      pyautogui.press('right')
    elif(isUp[0]):
      pyautogui.press('left')

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

  image.flags.writeable = False
  results = hands.process(image)

  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      fingers = []
      isUp=[False,False,False,False,False]
      # Track fingers
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
      if(mode==0):
        pyautogui.moveTo(fingers[1][0]*1920/640, fingers[1][1]*1080/480)
        mouse_buttons(isUp)
      elif(mode==1):
        gesture(angle, dist, isUp)
      
      elif(mode==2):
        tetris(isUp)
        
  cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
hands.close()
cap.release()
