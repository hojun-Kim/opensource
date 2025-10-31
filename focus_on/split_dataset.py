# 파일명: split_dataset.py
# ------------------------------------------------
# 'Drowsy', 'neutral' 같은 원본 폴더의 이미지들을
# 'train/1_drowsy', 'validation/1_drowsy' 등으로
# 랜덤하게 복사/분배하는 스크립트
# ------------------------------------------------

import os
import glob
import random
import shutil

# --- 1. ⚠️ 설정 (사용자 환경에 맞게 확인) ---

# 1. 기본 폴더 경로 (Drowsy, neutral 폴더가 있는 곳)
# (Windows 경로는 문자열 앞에 r을 붙여주세요)
BASE_DIR = r"C:\Users\hojun3909\Documents\오픈소스프로그래밍\dataset_3class"

# 2. 분배할 원본 폴더 이름 리스트
# (나중에 'Boredom'을 추가하면 여기에 'Boredom'을 넣으면 됩니다)
SOURCE_FOLDER_NAMES = ['Drowsy', 'neutral']

# 3. (중요) 원본 폴더명을 -> 최종 학습 폴더명으로 매핑
# (2단계 train_model.py가 인식할 폴더명입니다)
CLASS_MAP = {
    'Drowsy': '1_drowsy',
    'neutral': '2_neutral',
    # 'Boredom': '0_boredom' # 나중에 'Boredom' 폴더를 만들면 이 줄의 주석을 푸세요.
}

# 4. 학습/검증 데이터 분배 비율 (80%를 train으로)
TRAIN_RATIO = 0.8

# 5. 최종 목적지 폴더
DEST_TRAIN_DIR = os.path.join(BASE_DIR, 'train')
DEST_VALID_DIR = os.path.join(BASE_DIR, 'validation')

# --- 2. 스크립트 실행 ---

print("데이터 분배를 시작합니다...")

for source_name in SOURCE_FOLDER_NAMES:
    if source_name not in CLASS_MAP:
        print(f"'{source_name}'에 대한 CLASS_MAP 설정이 없습니다. 건너뜁니다.")
        continue

    # (1) 정보 설정
    final_class_name = CLASS_MAP[source_name] # 예: '1_drowsy'
    source_path = os.path.join(BASE_DIR, source_name)
    
    if not os.path.isdir(source_path):
        print(f"  [경고] 원본 폴더를 찾을 수 없습니다: {source_path}. 건너뜁니다.")
        continue

    # (2) 이미지 파일 개수 세기 (jpg, png, jpeg)
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
    all_images = []
    for ext in image_extensions:
        all_images.extend(glob.glob(os.path.join(source_path, ext)))
    
    total_images = len(all_images)
    if total_images == 0:
        print(f"  [정보] '{source_name}' 폴더에 이미지가 없습니다.")
        continue
        
    print(f"\n--- '{source_name}' 클래스 처리 중 ---")
    print(f"  총 {total_images}개의 이미지를 찾았습니다.")

    # (3) 랜덤으로 섞기
    random.shuffle(all_images)
    
    # (4) 비율에 맞게 분리
    split_point = int(total_images * TRAIN_RATIO)
    train_images = all_images[:split_point]
    valid_images = all_images[split_point:]
    
    # (5) 최종 목적지 폴더 생성
    final_train_path = os.path.join(DEST_TRAIN_DIR, final_class_name)
    final_valid_path = os.path.join(DEST_VALID_DIR, final_class_name)
    
    os.makedirs(final_train_path, exist_ok=True)
    os.makedirs(final_valid_path, exist_ok=True)
    
    # (6) 파일 복사 실행
    print(f"  -> {len(train_images)}개의 이미지를 'train/{final_class_name}'(으)로 복사합니다...")
    for img_path in train_images:
        shutil.copy2(img_path, final_train_path) # copy2는 메타데이터도 보존
        
    print(f"  -> {len(valid_images)}개의 이미지를 'validation/{final_class_name}'(으)로 복사합니다...")
    for img_path in valid_images:
        shutil.copy2(img_path, final_valid_path)
        
print("\n--- ✅ 모든 작업 완료 ---")