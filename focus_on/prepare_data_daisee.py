# 파일명: prepare_data_daisee.py (경로 수정본)
# ------------------------------------------------
# DAiSEE 데이터셋의 CSV 라벨과 파일 구조를 기반으로
# 4가지 감정 클래스의 이미지 폴더를 생성하는 1단계 스크립트
# ------------------------------------------------

import pandas as pd
import os
import cv2
import numpy as np

# --- ⚠️ 1. 중요 설정 (사용자 환경에 맞게 수정) ---

# DAiSEE 데이터셋을 다운로드한 최상위 폴더 경로
# (예: "C:/Users/hojun3909/Documents/오픈소스프로그래밍/dataset/DAiSEE")
# (참고: 경로 문자열 앞에 r을 붙이거나, / 를 사용하세요)
DAISEE_ROOT_FOLDER = r"C:\Users\hojun3909\Documents\오픈소스프로그래밍\dataset\DAiSEE" 

# 라벨 파일이 있는 폴더
LABELS_FOLDER = os.path.join(DAISEE_ROOT_FOLDER, "Labels")

# +++ 수정: 'DataSet' (대문자 S)로 변경 +++
VIDEO_ROOT_FOLDER = os.path.join(DAISEE_ROOT_FOLDER, "DataSet")

# 전처리된 얼굴 이미지를 저장할 최종 폴더
OUTPUT_DATASET_PATH = "./dataset_daisee_4class" # (이전과 겹치지 않게 이름 변경)

# 이 스크립트가 분류할 감정 라벨 (CSV 컬럼명과 일치해야 함)
EMOTION_LABELS = ['Boredom', 'Engagement', 'Confusion', 'Frustration']

# 저장할 폴더명 매핑
CLASS_MAP = {
    'Boredom': '0_boredom',
    'Engagement': '1_engagement',
    'Confusion': '2_confusion',
    'Frustration': '3_frustration'
}

# --- 2. 전처리에 필요한 도구 ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
FRAME_INTERVAL = 10 # 10 프레임마다 1장씩 저장

# --- 3. 폴더 생성 함수 ---
def create_folders():
    print(f"출력 폴더를 '{OUTPUT_DATASET_PATH}'에 생성합니다...")
    for split in ['train', 'validation']:
        for folder_name in CLASS_MAP.values():
            folder_path = os.path.join(OUTPUT_DATASET_PATH, split, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
    print("출력 폴더 생성 완료.")

# --- 4. 비디오 처리 함수 ---
def process_videos(split_name, labels_df):
    """
    라벨 CSV(DataFrame)를 기반으로 비디오를 처리하고 얼굴 이미지를 저장합니다.
    """
    video_path_column = 'ClipID'
    total_videos = len(labels_df)
    total_saved_images = 0
    
    print(f"\n--- {split_name} 데이터셋 처리 시작 (총 {total_videos}개 비디오) ---")

    for index, row in labels_df.iterrows():
        clip_filename = row[video_path_column] # 예: '1100011002.avi'
        
        # +++ 수정: ClipID로부터 경로 조합 +++
        try:
            subject_id = clip_filename[:6] # 예: '110001'
            video_id_folder = os.path.splitext(clip_filename)[0] # 예: '1100011002'
            
            # 경로 조합: '110001' / '1100011002' / '1100011002.avi'
            video_relative_path = os.path.join(subject_id, video_id_folder, clip_filename)
        except Exception as e:
            print(f"  [경고] '{clip_filename}'에서 경로 추출 실패: {e}")
            continue

        # (1) 비디오 전체 경로
        video_full_path = os.path.join(VIDEO_ROOT_FOLDER, split_name.capitalize(), video_relative_path)
        
        if not os.path.exists(video_full_path):
            # (디버깅) 경로가 틀렸을 경우를 대비해 한번 더 체크
            # print(f"  [경고] 비디오 파일을 찾을 수 없음: {video_full_path}")
            continue

        # (2) 라벨 판정: 4개 감정 중 가장 점수가 높은 감정을 선택
        scores = row[EMOTION_LABELS].values
        dominant_emotion_index = np.argmax(scores)
        dominant_emotion = EMOTION_LABELS[dominant_emotion_index]

        # (3) 저장할 폴더 결정
        save_folder_name = CLASS_MAP[dominant_emotion]
        save_path = os.path.join(OUTPUT_DATASET_PATH, split_name, save_folder_name)

        # (4) 비디오 열기 및 프레임 추출
        cap = cv2.VideoCapture(video_full_path)
        frame_count = 0
        saved_count_in_video = 0

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
                    
                    # 파일명 (비디오명 + 프레임번호)
                    safe_filename = f"{video_id_folder}_frame{frame_count}.jpg"
                    
                    cv2.imwrite(os.path.join(save_path, safe_filename), resized_face)
                    saved_count_in_video += 1
                    total_saved_images += 1
                    break 
                except Exception as e:
                    pass 
        
        cap.release()
        
        if (index + 1) % 100 == 0:
            print(f"  ... {index + 1}/{total_videos} 처리 완료 (현재까지 총 {total_saved_images}개 이미지 저장)")

    print(f"--- {split_name} 처리 완료 (총 {total_saved_images}개 이미지) ---")

# --- 5. 메인 스크립트 실행 ---
if __name__ == "__main__":
    create_folders()
    
    # +++ 수정: CSV 컬럼명의 공백 제거 (예: 'Frustration ') +++
    def load_labels_csv(path):
        try:
            df = pd.read_csv(path)
            # 컬럼명 앞뒤 공백 제거
            df.columns = df.columns.str.strip()
            # EMOTION_LABELS에 해당하는 컬럼이 있는지 확인
            for col in EMOTION_LABELS:
                if col not in df.columns:
                    print(f"오류: CSV 파일에 '{col}' 컬럼이 없습니다. 실제 컬럼: {df.columns.tolist()}")
                    return None
            return df
        except FileNotFoundError:
            print(f"오류: {path} 파일을 찾을 수 없습니다.")
            return None
        except Exception as e:
            print(f"오류 ({path}): {e}")
            return None

    # (1) 학습 데이터(Train) 처리
    train_labels_path = os.path.join(LABELS_FOLDER, "TrainLabels.csv")
    train_df = load_labels_csv(train_labels_path)
    if train_df is not None:
        process_videos('train', train_df)

    # (2) 검증 데이터(Validation) 처리
    valid_labels_path = os.path.join(LABELS_FOLDER, "ValidationLabels.csv")
    valid_df = load_labels_csv(valid_labels_path)
    if valid_df is not None:
        process_videos('validation', valid_df)
        
    print("\n--- 모든 데이터 전처리 완료 ---")