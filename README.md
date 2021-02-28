# Open source Kinect
Is a project that brings the joy of augmented reality (AR) gaming to your windows PC completely open source.
But it is so much more than that.
## No mouse? No problem
With the open source kinect, you can also control your PC just as you would using your mouse. (Only without a mouse!!)
## Too lazy to reach all the way to your mouse?
Using the gesture mode of the open source kinect, you can do tasks like change system volume, navigate between windows and tabs, just with a flick of your hand!
## Technologies used:
1. python 3.*
2. pyautogui - used to navigate through the user's system
3. openCV - used to capture the user's gestures
4. mediapipe - used to track the user's hand
# Installation
1. clone this repository on your system
2. install python libraries pyautogui and opencv-python (pip install should do the trick)
# Usage
## Mouse mode:
* run handpose.py
* select 'mode 0'
* hold out index finger and move it to move your cursor
* hold out both index and middle finger to right click
* hold out both index and ring finger to left click
* hold out all four fingers (not the thumb) to scroll up and down
## Gesture mode:
* run handpose.py
* select 'mode 1'
* hold out index finger and move it up and down to control the volume of your system
* hold out both index and middle fingers and move them right or left to cycle between windows (like alt + tab)
* hold out index, middle and ring fingers and move them right or left to cycle between tabs (like ctrl + tab)
## tetris mode:
* run handpose.py
* select 'mode 2'
* go to https://bitoffabyte.github.io/React-Tetris/ (open source browser based tetris game)
* press spacebar/enter to start
* hold out index finger to take contol
* hold out both index and middle finger to move the piece to the right
* hold out both index finger and thumb to move the piece to the left
* hold out index, middle and ring finger to push the piece down 
* hold out all four fingers (except thumb) to change orientation of the piece
