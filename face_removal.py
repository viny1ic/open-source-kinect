import cv2

def remove_face(img):

    face_cascade = cv2.CascadeClassifier('face_detect.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        img[y-10:(y+h+20), x-10:(x+w+20), :] = [0, 0, 0]

    return img

# cap = cv2.VideoCapture(0)
# while True:
#     _, img = cap.read()
#     img = remove_face(img)
#
#     cv2.imshow("win", cv2.flip(img, 1))
#     cv2.waitKey(1)