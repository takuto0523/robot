import numpy as np
import cv2

# カメラキャリブレーションで得られた内部パラメータと歪み係数
mtx = np.array([[489.19077753, 0, 321.92789238], [0, 486.75540111, 250.06278134], [0, 0, 1]])  # カメラマトリックス

# ボールの実際の直径と半径（ミリメートル）
real_diameter = 67  # 例: 6.7cm = 67mmのボール
real_radius = real_diameter / 2  # ボールの半径

# カメラの高さ [mm]
camera_height = 35  # 240mmの高さに設置

# カメラ角度 [rad]
camera_angle = np.deg2rad(24)  # 地面と平行

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
        if radius > 10:  # 適当な最小半径の閾値を設定
            return (int(x), int(y)), int(radius)
    return None, None

def calculate_distance(focal_length, real_radius, camera_height, camera_angle, fy, yi, cx, cy):
    # ボールとカメラのなす角 [rad]
    yy = (yi - cy) / fy
    theta_c = np.arctan(yy) # yiはボールの中心点
    theta = camera_angle - theta_c 
    # グローバル座標系でのボールの中心点の座標 [mm]
    yw = (camera_height - real_radius) / np.tan(theta)
    return yw

def main():
    # 画像をキャプチャ
    capture_image()

    # キャプチャした画像を読み込む
    img = cv2.imread('ball_image.jpg')

    # ボールを検出
    center, radius = detect_ball(img)
    if center is not None and radius is not None:
        xi, yi = center

        # 焦点距離 [pixel]
        fy = mtx[1, 1]
        focal_length = mtx[0, 0]

        # 画像中心の座標 [pixel]
        cx, cy = mtx[0, 2], mtx[1, 2]

        # 距離を計算
        distance = calculate_distance(focal_length, real_radius, camera_height, camera_angle, fy, yi, cx, cy)
        print(f"Ball distance (yw): {distance:.2f} mm")
    else:
        print("Ball not detected")

if __name__ == "__main__":
    main()
