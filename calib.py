import cv2
import numpy as np
import glob

# チェスボードのサイズ
chessboard_size = (10, 7)

# チェスボードの1つのマスの物理的な大きさ (例: 25mm = 0.025m)
square_size = 0.025  # メートル

# チェスボードの各コーナーの3Dポイント (物理的なサイズで指定)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# 3Dポイントと2D画像ポイントの配列を保存するリスト
objpoints = []
imgpoints = []

# キャリブレーション画像のパスを取得
images = glob.glob('/home/takuto/robokon/.venv/robo/calibration_images/*.jpg')

if len(images) == 0:
    print("No calibration images found in the specified directory.")
    exit()

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # チェスボードのコーナーを見つける
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
    # コーナーが見つかった場合、配列に追加
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        
        # コーナーを描画する
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)
    else:
        print(f"Chessboard corners not found in image: {fname}")

cv2.destroyAllWindows()

# キャリブレーションの入力データがあるか確認
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("No valid calibration data found. Ensure that the images contain a visible chessboard pattern.")
    exit()

# キャリブレーションを行う
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("内部パラメータ（カメラマトリックス）:\n", mtx)
print("歪み係数:\n", dist)
