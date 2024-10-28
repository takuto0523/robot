import cv2
import numpy as np

def pick_up_colored_balls():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

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

        # Define color ranges
        lower_blue = np.array([100, 70, 70])
        upper_blue = np.array([150, 255, 255])

        lower_red = np.array([150, 104, 70])
        upper_red = np.array([180, 255, 255])

        lower_yellow = np.array([10, 74, 130])
        upper_yellow = np.array([50, 255, 240])

        # Create masks
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply masks
        img_blue = cv2.bitwise_and(img, img, mask=mask_blue)
        img_red = cv2.bitwise_and(img, img, mask=mask_red)
        img_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

        # Hough transformation
        img = img[:, ::-1]

        for img_color, mask, color_name in [(img_blue, mask_blue, 'Blue'), (img_red, mask_red, 'Red'), (img_yellow, mask_yellow, 'Yellow')]:
            img_color = cv2.resize(img_color, size)
            img_color = cv2.GaussianBlur(img_color, (15, 15), 1)  # ガウシアンブラーを適用

            cimg2 = img_color

            img_color = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
            circles = cv2.HoughCircles(img_color, cv2.HOUGH_GRADIENT, 1, 20, param1=25, param2=23, minRadius=5, maxRadius=150)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # Draw the outer circle
                    cv2.circle(cimg1, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # Draw the center of the circle
                    cv2.circle(cimg1, (i[0], i[1]), 2, (0, 0, 255), 3)
            else:
                print(f"nothing {color_name}")

            cv2.imshow(f'{color_name} Mask', cimg2)

        cv2.imshow('Original', cimg1)
        k = cv2.waitKey(10)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pick_up_colored_balls()