import numpy as np
import cv2

# カメラキャリブレーションで得られた内部パラメータと歪み係数
mtx = np.array([[489.19077755, 0, 321.92789236], [0, 486.75540112, 250.062781328], [0, 0, 1]])  # カメラマトリックス
dist = np.array([0.06273926, 0.2188829, -0.00193607, 0.00228626, -0.77372788])  # 歪み係数

# ボールの実際の直径と半径（メートル）
real_diameter = 0.67  # 例: 67cmのボール
real_radius = real_diameter / 2

# カメラの高さ [mm]
camera_height = 47  # 例: 0.042メートルの高さに設置

# カメラ角度 [rad]
camera_angle = np.deg2rad(90)  # 例: 30度の角度で設置

# キャプチャした画像の読み込み
img = cv2.imread('captured_image.jpg')

# 画像の歪み補正
h, w = img.shape[:2]
new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
undistorted_img = cv2.undistort(img, mtx, dist, None, new_camera_mtx)

# ボールを検出
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

center, radius = detect_ball(undistorted_img)
if center is not None and radius is not None:
    xi, yi = center

    # 焦点距離 [pixel]
    f_pixel = mtx[0, 0]

    # ボールとカメラのなす角 [rad]
    theta_c = np.arctan2(yi, f_pixel)

    # グローバル座標系でのボールの中心点の座標 [mm]
    yw = (camera_height - real_radius) / np.tan(camera_angle - theta_c)

    print(f"Ball distance (yw): {yw:.2f} mm")
else:
    print("Ball not detected")
