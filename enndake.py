import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frameWidth = 640
frameHeight = 480

def nothing(x):
    pass

cv2.namedWindow('trackbar')

# トラックバーを作成
cv2.createTrackbar("param1", "trackbar", 10, 100, nothing)
cv2.createTrackbar("param2", "trackbar", 25, 100, nothing)
cv2.createTrackbar("minRadius", "trackbar", 25, 100, nothing)
cv2.createTrackbar("maxRadius", "trackbar", 35, 100, nothing)

cv2.createTrackbar("H_l", "trackbar", 0, 180, nothing)
cv2.createTrackbar("S_l", "trackbar", 0, 255, nothing)
cv2.createTrackbar("V_l", "trackbar", 0, 255, nothing)
cv2.createTrackbar("H_h", "trackbar", 255, 180, nothing)
cv2.createTrackbar("S_h", "trackbar", 255, 255, nothing)
cv2.createTrackbar("V_h", "trackbar", 255, 255, nothing)

while True:
    ret, frame = cap.read()

    if ret:
        frame = cv2.resize(frame, (frameWidth, frameHeight))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # トラックバーの値を取得
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

        gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        param1 = cv2.getTrackbarPos("param1", "trackbar")
        param2 = cv2.getTrackbarPos("param2", "trackbar")
        minRadius = cv2.getTrackbarPos("minRadius", "trackbar")
        maxRadius = cv2.getTrackbarPos("maxRadius", "trackbar")

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, frame.shape[0] // 8,
                                   param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # 円の外側の輪郭を描画
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # 円の中心を描画
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        cv2.imshow("origin", frame)
        cv2.imshow("mask_image", frame_color)

        k = cv2.waitKey(10)
        if k == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
