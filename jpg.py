import os
import shutil

def move_jpg_files(source_dir, target_dir):
    # ホームディレクトリを含むパスを展開
    source_dir = os.path.expanduser(source_dir)
    target_dir = os.path.expanduser(target_dir)

    # ソースディレクトリが存在するか確認
    if not os.path.exists(source_dir):
        print(f'Source directory does not exist: {source_dir}')
        return

    # ソースディレクトリからすべてのファイルを取得
    files = os.listdir(source_dir)

    # ターゲットディレクトリが存在しない場合、作成
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 各ファイルを確認し、.jpg拡張子のファイルを移動
    for file in files:
        if file.lower().endswith('.jpg'):
            source_path = os.path.join(source_dir, file)
            target_path = os.path.join(target_dir, file)
            shutil.move(source_path, target_path)
            print(f'Moved: {file}')

# ソースディレクトリとターゲットディレクトリを指定
source_directory = '~/robokon/.venv/robo/caalibration_images'
target_directory = '~/robokon/.venv/robo/calibration_images'

move_jpg_files(source_directory, target_directory)
