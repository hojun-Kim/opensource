# 파일명: prepare_boredom_only.py
# ------------------------------------------------
# DAiSEE 데이터셋에서 'Boredom' 점수가 높은 (>= 2)
# 비디오만 찾아서, 'dataset_3class' 폴더의 '0_boredom'으로
# 얼굴 이미지를 추출/저장하는 스크립트
# ------------------------------------------------

import pandas as pd
import os
import cv2
import numpy as np

# --- ⚠️ 1. 중요 설정 (사용자 환경에 맞게 수정) ---

# DAiSEE 데이터셋을 다운로드한 최상위 폴더 경로
# (내부에 'DataSet', 'Labels' 폴더가 있는 곳)
# (예: "C:/Users/hojun3909/Documents/오픈소스프로그래밍/dataset/DAiSEE")
DAISEE_ROOT_FOLDER = r"C:\Users\hojun3909\Documents\오픈소스프로그래밍\dataset\DAiSEE" 

# 최종 이미지를 저장할 'dataset_3class' 폴더 경로
# (내부에 'train', 'validation' 폴더가 있는 곳)
# (예: "C:/Users/hojun3909/Documents/오픈소스프로그래밍/dataset_3class")
OUTPUT_DATASET_PATH = r"C:\Users\hojun3909\Documents\오픈소스프로그래밍\dataset_3class"

# 'Boredom' 점수 임계값 (2: high, 3: very high)
BOREDOM_THRESHOLD = 2

# --- 2. 경로 및 도구 설정 ---
LABELS_FOLDER = os.path.join(DAISEE_ROOT_FOLDER, "Labels")
VIDEO_ROOT_FOLDER = os.path.join(DAISEE_ROOT_FOLDER, "DataSet")

# 저장할 최종 폴더명
FINAL_CLASS_NAME = '0_boredom'

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
FRAME_INTERVAL = 10 # 10 프레임마다 1장씩 저장

# --- 3. 비디오 처리 함수 ---
def process_boredom_videos(split_name, labels_df):
    """
    라벨 CSV(DataFrame)를 기반으로 'Boredom' 비디오만 처리합니다.
    """
    
    # (1) 'Boredom' 점수가 임계값 이상인 비디오만 필터링
    bored_videos_df = labels_df[labels_df['Boredom'] >= BOREDOM_THRESHOLD]
    
    total_videos = len(bored_videos_df)
    total_saved_images = 0
    
    if total_videos == 0:
        print(f"  [정보] {split_name}에서 'Boredom >= {BOREDOM_THRESHOLD}'인 비디오를 찾지 못했습니다.")
        return

    print(f"\n--- {split_name} 'Boredom' 데이터 처리 시작 (총 {total_videos}개 비디오) ---")

    # (2) 저장할 폴더 생성 (예: .../dataset_3class/train/0_boredom)
    save_path = os.path.join(OUTPUT_DATASET_PATH, split_name, FINAL_CLASS_NAME)
    os.makedirs(save_path, exist_ok=True)

    video_path_column = 'ClipID' 

    for index, row in bored_videos_df.iterrows():
        clip_filename = row[video_path_column] # 예: '1100011002.avi'
        
        try:
            subject_id = clip_filename[:6] # 예: '110001'
            video_id_folder = os.path.splitext(clip_filename)[0] # 예: '1100011002'
            video_relative_path = os.path.join(subject_id, video_id_folder, clip_filename)
        except Exception as e:
            print(f"  [경고] '{clip_filename}'에서 경로 추출 실패: {e}")
            continue

        video_full_path = os.path.join(VIDEO_ROOT_FOLDER, split_name.capitalize(), video_relative_path)
        
        if not os.path.exists(video_full_path):
            continue

        # (3) 비디오 열기 및 프레임 추출
        cap = cv2.VideoCapture(video_full_path)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret: break
            frame_count += 1
            if frame_count % FRAME_INTERVAL != 0: continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(48, 48))

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                try:
                    resized_face = cv2.resize(roi_gray, (48, 48))
                    safe_filename = f"{video_id_folder}_frame{frame_count}.jpg"
                    
                    cv2.imwrite(os.path.join(save_path, safe_filename), resized_face)
                    total_saved_images += 1
                    break 
                except Exception as e:
                    pass 
        
        cap.release()
        
        if (index + 1) % 50 == 0:
            print(f"  ... {index + 1}/{total_videos} 처리 완료 (현재까지 총 {total_saved_images}개 이미지 저장)")

    print(f"--- {split_name} 처리 완료 (총 {total_saved_images}개 'Boredom' 이미지) ---")

# --- 4. CSV 로드 함수 (컬럼 공백 제거 포함) ---
def load_labels_csv(path):
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip() # 'Boredom' 등 컬럼명 공백 제거
        if 'Boredom' not in df.columns or 'ClipID' not in df.columns:
            print(f"오류: {path}에 'ClipID' 또는 'Boredom' 컬럼이 없습니다.")
            return None
        return df
    except FileNotFoundError:
        print(f"오류: {path} 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"오류 ({path}): {e}")
        return None

# --- 5. 메인 스크립트 실행 ---
if __name__ == "__main__":
    print(f"DAiSEE 'Boredom' 데이터 추출을 시작합니다 (임계값: {BOREDOM_THRESHOLD}).")
    
    # (1) 학습 데이터(Train) 처리
    train_labels_path = os.path.join(LABELS_FOLDER, "TrainLabels.csv")
    train_df = load_labels_csv(train_labels_path)
    if train_df is not None:
        process_boredom_videos('train', train_df)

    # (2) 검증 데이터(Validation) 처리
    valid_labels_path = os.path.join(LABELS_FOLDER, "ValidationLabels.csv")
    valid_df = load_labels_csv(valid_labels_path)
    if valid_df is not None:
        process_boredom_videos('validation', valid_df)
        
    print("\n--- ✅ 'Boredom' 데이터 추출 완료 ---")