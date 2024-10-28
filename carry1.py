import cv2
import numpy as np

def calibrate_wall_color(hsv_wall_color):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # カメラの幅
    cap.set(4, 480)  # カメラの高さ

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # HSV色空間に変換
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 壁の色に近い色の範囲を定義
        lower_wall_color = np.array([hsv_wall_color[0] - 10, max(0, hsv_wall_color[1] - 50), max(0, hsv_wall_color[2] - 50)])
        upper_wall_color = np.array([hsv_wall_color[0] + 10, min(255, hsv_wall_color[1] + 50), min(255, hsv_wall_color[2] + 50)])

        # 壁の色に対応するマスクを作成
        mask_wall_color = cv2.inRange(hsv_frame, lower_wall_color, upper_wall_color)

        # マスクを元のフレームに適用して壁の色の領域を抽出
        result_frame = cv2.bitwise_and(frame, frame, mask=mask_wall_color)

        # 結果を表示
        cv2.imshow('Calibrated Wall Color', result_frame)
        
        # キー入力を待機し、'q'が押されたら終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 壁の色のHSV値
    hsv_wall_color = np.array([25, 160, 158])

    # キャリブレーションの実行
    calibrate_wall_color(hsv_wall_color)
