import cv2
import numpy as np

def pick_up_colored_balls():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # Define color range for yellow (wall color)
    lower_yellow = np.array([10, 74, 130])
    upper_yellow = np.array([50, 255, 240])

    while True:
        ret, img = cap.read()
        if not ret:
            break

        size = (640, 480)
        cimg1 = img.copy()

        # ノイズ除去
        img = cv2.medianBlur(img, 5)  # メディアンブラーを適用

        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Create mask for yellow color
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply mask
        img_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

        # Hough transformation
        img = img[:, ::-1]

        img_yellow = cv2.resize(img_yellow, size)
        img_yellow = cv2.GaussianBlur(img_yellow, (15, 15), 1)  # ガウシアンブラーを適用

        cimg2 = img_yellow

        img_yellow = cv2.cvtColor(img_yellow, cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(img_yellow, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=23, minRadius=5, maxRadius=150)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Draw the outer circle
                cv2.circle(cimg1, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Draw the center of the circle
                cv2.circle(cimg1, (i[0], i[1]), 2, (0, 0, 255), 3)
        else:
            print("nothing detected")

        cv2.imshow('Yellow Mask', cimg2)
        cv2.imshow('Original', cimg1)
        k = cv2.waitKey(10)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pick_up_colored_balls()
