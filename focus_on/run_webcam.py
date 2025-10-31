# 파일명: run_webcam.py (3-Class 최종본)
# ------------------------------------------------
# 'emotion_model_3class.h5' (86.5% 정확도) 모델을 사용하여
# Boredom, Drowsy, Neutral을 실시간으로 분석합니다.
# ------------------------------------------------

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time
import matplotlib.pyplot as plt
from collections import Counter # 비율 그래프(파이 차트)용

# --- 1. 모델 및 설정 불러오기 ---

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# +++ 1. 새로 학습한 3-Class 모델 로드 +++
try:
    model = load_model('emotion_model_3class.h5')
except Exception as e:
    print(f"오류: 'emotion_model_3class.h5' 모델을 불러올 수 없습니다.")
    print("2단계 'train_model.py'를 먼저 실행하여 모델을 생성하세요.")
    exit()

# +++ 2. 라벨 리스트 변경 (train_model.py의 출력 순서와 동일해야 함) +++
# ⚠️ 중요: {'0_boredom': 0, '1_drowsy': 1, '2_neutral': 2} 순서 확인!
emotion_labels = ['Boredom', 'Drowsy', 'Neutral']

IMG_HEIGHT = 48
IMG_WIDTH = 48

# +++ 3. '집중도' 기준을 'Neutral'로 변경 +++
try:
    NEUTRAL_INDEX = emotion_labels.index('Neutral')
except ValueError:
    print(f"오류: emotion_labels 리스트에 'Neutral'이 없습니다.")
    exit()

# --- 알림 및 시각화 변수 ---
alert_status = False
alert_start_time = None
ALERT_DURATION_THRESHOLD = 3 # 3초간 지속되면 알림

concentration_log = [] # (1) 선 그래프용 (Neutral 확률)
emotion_pie_log = []   # (2) 원 그래프용 (1등 감정 이름)

program_start_time = time.time()
last_sample_time = program_start_time
SAMPLE_INTERVAL = 1.0 # 1.0초마다 데이터 샘플링

# --- 2. 웹캠 실행 및 실시간 처리 ---

print("웹캠을 시작합니다... (종료하려면 'q' 키를 누르세요)")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("오류: 웹캠 프레임을 읽을 수 없습니다.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    current_face_emotion = None
    current_prediction_probs = None 

    for (x, y, w, h) in faces:
        # (얼굴 영역 처리)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w] 
        roi_gray = cv2.resize(roi_gray, (IMG_WIDTH, IMG_HEIGHT))
        roi = roi_gray.astype('float') / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)

        # (모델 예측)
        prediction = model.predict(roi, verbose=0)[0] # (1, 3) 확률 반환
        
        if current_prediction_probs is None:
            current_prediction_probs = prediction 

        emotion_index = np.argmax(prediction)
        confidence = prediction[emotion_index] * 100
        emotion_text = emotion_labels[emotion_index] # +++ 3개 라벨 중 하나가 표시됨 +++
        
        text_to_show = f"{emotion_text} ({confidence:.1f}%)"
        cv2.putText(frame, text_to_show, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if current_prediction_probs is not None:
        current_face_emotion = emotion_labels[np.argmax(current_prediction_probs)]

    # +++ 4. 이벤트 발생 로직 변경 (원래 목표) +++
    # 'Boredom' 또는 'Drowsy'가 감지되면 알림 시작
    if current_face_emotion in ['Boredom', 'Drowsy']:
        if alert_status == False:
            alert_status = True
            alert_start_time = time.time()
        else:
            duration = time.time() - alert_start_time
            if duration > ALERT_DURATION_THRESHOLD:
                cv2.putText(frame, "!! ALERT: Take a Rest !!", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    else:
        # 'Neutral' 이거나 얼굴이 없으면 초기화
        alert_status = False
        alert_start_time = None
        
    
    # --- 5. 집중도 데이터 샘플링 ---
    current_time = time.time()
    if current_time - last_sample_time >= SAMPLE_INTERVAL:
        elapsed_time = current_time - program_start_time
        
        # (1) 선 그래프용: 'Neutral' 확률을 '집중도 점수'로 사용
        concentration_score = 0.0 
        if current_prediction_probs is not None:
            concentration_score = current_prediction_probs[NEUTRAL_INDEX] 
        concentration_log.append((elapsed_time, concentration_score))
        
        # (2) 원 그래프용: 1등 감정 이름 저장
        if current_face_emotion is not None:
            emotion_pie_log.append(current_face_emotion)
        else:
            emotion_pie_log.append("No_Face_Detected")
            
        last_sample_time = current_time

    # --- 6. 화면 출력 ---
    cv2.imshow('Real-time Emotion Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 7. 종료 처리 ---
print("프로그램을 종료합니다.")
cap.release()
cv2.destroyAllWindows()


# --- 8. 최종 집중도 그래프 시각화 (선 그래프) ---
print("집중도(Neutral) 선 그래프를 생성합니다...")
if not concentration_log:
    print("기록된 데이터가 없습니다.")
else:
    timestamps, scores = zip(*concentration_log)
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, scores, marker='.', linestyle='-', label='Concentration (Neutral Prob.)')
    
    plt.title("Concentration Level Over Time", fontsize=16)
    plt.xlabel("Time (seconds)", fontsize=12)
    plt.ylabel("Concentration Score (0.0 to 1.0)", fontsize=12)
    
    plt.ylim(0, 1.05) 
    plt.xlim(left=0)  
    plt.grid(True)    
    
    average_score = np.mean(scores)
    plt.axhline(y=average_score, color='r', linestyle='--', label=f'Average: {average_score:.2f}')
    plt.legend()
    
    print(f"평균 집중도 점수: {average_score:.2f}")
    plt.show() # 첫 번째 그래프(선) 표시


# --- 9. 최종 감정 비율 그래프 시각화 (원 그래프) ---
print("전체 감정 비율 원 그래프를 생성합니다...")
if not emotion_pie_log:
    print("기록된 감정 데이터가 없습니다.")
else:
    emotion_counts = Counter(emotion_pie_log)
    labels = list(emotion_counts.keys())
    sizes = list(emotion_counts.values())

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title("Overall Emotion Ratio (3-Class)", fontsize=16)
    plt.axis('equal')  
    
    print(f"감정 비율 집계: {emotion_counts}")
    plt.show() # 두 번째 그래프(원) 표시