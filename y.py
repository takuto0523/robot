import cv2
import math
import numpy as np

# カメラキャリブレーションで得られた内部パラメータと歪み係数
mtx = np.array([[489.19077755, 0, 321.92789236], 
                [0, 486.75540112, 250.062781328], 
                [0, 0, 1]])  # カメラマトリックス
dist = np.array([0.06273926, 0.2188829, -0.00193607, 0.00228626, -0.77372788])  # 歪み係数

# ボールの実際の直径（メートル）
real_diameter = 0.66  # 例: 0.67mのボール
r = real_diameter / 2

# カメラの角度
t = 30

# カメラの高さ
l = 245

def capture_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.imwrite('ball_image.jpg', frame)
                break
    cap.release()
    cv2.destroyAllWindows()

def detect_ball(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([150, 104, 70])
    upper_red = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        if radius > 10:
            return (int(x), int(y)), int(radius)
    return None, None

def calculate_camera_coordinates(center, mtx):
    cx = mtx[0, 2]
    cy = mtx[1, 2]
    fx = mtx[0, 0]
    fy = mtx[1, 1]
    xi = (center[0] - cx) / fx
    yi = (center[1] - cy) / fy



    return yi

def calculate_physical_length(yi):
    theta_c = np.arctan(yi)
    y1 = np.tan(np.radians(t) - theta_c)
    yw = (l - r) / y1
    return yw


def main():
    capture_image()

    img = cv2.imread('ball_image.jpg')
    

    center, radius = detect_ball(undistorted_img)
    if center is not None and radius is not None:
        cv2.circle(undistorted_img, center, radius, (0, 255, 0), 2)
        cv2.imshow("Detected Ball", undistorted_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        y1 = calculate_camera_coordinates(center, mtx)  # y1を計算
        yw = calculate_physical_length(y1)
        print(f"Ball center in camera coordinates: yw: {yw:.2f}")
    else:
        print("Ball not detected")

if __name__ == "__main__":
    main()