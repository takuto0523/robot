import cv2
import numpy as np
cap = cv2.VideoCapture(0)
frameWidth = 640
frameHeight = 480

def nothing(x):
    pass
cv2.namedWindow('trackbar')

cv2.createTrackbar("H_l", "trackbar", 0, 180, nothing)
cv2.createTrackbar("S_l", "trackbar", 0, 255, nothing)
cv2.createTrackbar("V_l", "trackbar", 0, 255, nothing)
cv2.createTrackbar("H_h", "trackbar", 255, 180, nothing)
cv2.createTrackbar("S_h", "trackbar", 255, 255, nothing)
cv2.createTrackbar("V_h", "trackbar", 255, 255, nothing)
while (1):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (frameWidth, frameHeight))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_l = cv2.getTrackbarPos("H_l", "trackbar")
    h_h = cv2.getTrackbarPos("H_h", "trackbar")
    s_l = cv2.getTrackbarPos("S_l", "trackbar")
    s_h = cv2.getTrackbarPos("S_h", "trackbar")
    v_l = cv2.getTrackbarPos("V_l", "trackbar")
    v_h = cv2.getTrackbarPos("V_h", "trackbar")

    lower = np.array([h_l, s_l, v_l])
    upper = np.array([h_h, s_h, v_h])

    frame_mask = cv2.inRange(hsv, lower, upper)
    frame_color = cv2.bitwise_and(frame, frame, mask=frame_mask)
    
    cv2.imshow("origin", frame)
    cv2.imshow("mask_image", frame_color)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
# ----------- END OF FILE ------------