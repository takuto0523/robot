import cv2
import numpy as np

# カメラキャリブレーションで得られた内部パラメータと歪み係数
mtx = np.array([[489.19077755, 0, 321.92789236], [0, 486.75540112, 250.062781328], [0, 0, 1]])  # カメラマトリックス
dist = np.array([0.06273926, 0.2188829, -0.00193607, 0.00228626, -0.77372788])  # 歪み係数

# ボールの実際の直径（メートル）
real_diameter = 0.67  # 例: 67cmのボール

def capture_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.imwrite('ball_image.jpg', frame)
                print("Image captured and saved as 'ball_image.jpg'")
                break
    cap.release()
    cv2.destroyAllWindows()

def detect_ball(img):
    # ボール検出のための色空間変換とマスク処理（例: 赤いボールの場合）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([150, 104, 70])
    upper_red = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # マスク処理後の画像から輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        if radius > 10:  # 適当な最小半径の閾値を設定
            print(f"Ball detected at: ({x:.2f}, {y:.2f}) with radius: {radius:.2f}")
            return (int(x), int(y)), int(radius)
    print("No contours found or ball too small")
    return None, None

def calculate_distance(focal_length, real_diameter, perceived_diameter):
    # 三角測量の公式を使用して距離を計算
    return (real_diameter * focal_length) / perceived_diameter

def main():
    # 画像をキャプチャ
    capture_image()

    # キャプチャした画像を読み込む
    img = cv2.imread('ball_image.jpg')
    if img is None:
        print("Failed to load the captured image")
        return

    # 画像をリサイズして処理速度を向上させる（オプション）
    img = cv2.resize(img, (640, 480))

    # 画像の歪み補正
    h, w = img.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, mtx, dist, None, new_camera_mtx)
    print("Image undistorted")

    # ボールを検出
    center, radius = detect_ball(undistorted_img)
    if center is not None and radius is not None:
        cv2.circle(undistorted_img, center, radius, (0, 255, 0), 2)
        cv2.imshow("Detected Ball", undistorted_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # カメラの焦点距離を計算（事前に既知の場合はその値を使用）
        focal_length = mtx[0, 0]
        print(f"Focal length: {focal_length}")

        # 距離を計算
        perceived_diameter = radius * 2
        distance = calculate_distance(focal_length, real_diameter, perceived_diameter)
        print(f"Real diameter: {real_diameter} meters")
        print(f"Perceived diameter: {perceived_diameter} pixels")
        print(f"Ball distance: {distance:.2f} meters")
    else:
        print("Ball not detected")

if __name__ == "__main__":
    main()
