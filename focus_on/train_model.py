# 파일명: train_model.py
# ------------------------------------------------
# 'dataset_3class' 폴더 (Boredom, Drowsy, Neutral)를
# 읽어서 'emotion_model_3class.h5' 모델을 생성하는 스크립트
# ------------------------------------------------

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os

# --- 1. 기본 설정 ---
IMG_HEIGHT = 48
IMG_WIDTH = 48
BATCH_SIZE = 32 
EPOCHS = 100 # (EarlyStopping이 최적의 시점에 멈춰줄 것입니다)

# +++ 1단계에서 만든 새 데이터셋 폴더 경로 +++
base_dir = './dataset_3class' 
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# --- 2. 데이터 준비 (ImageDataGenerator) ---
# (이전과 동일)
train_datagen = ImageDataGenerator(
    rescale=1./255,            # 정규화
    rotation_range=30,       # 랜덤 회전
    width_shift_range=0.2,   # 랜덤 가로 이동
    height_shift_range=0.2,  # 랜덤 세로 이동
    shear_range=0.2,         # 랜덤 기울임
    zoom_range=0.2,          # 랜덤 줌
    horizontal_flip=True,    # 랜덤 좌우 반전
    fill_mode='nearest'
)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical', # 다중(3-class) 분류
    shuffle=True
)
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# +++ 자동으로 3개 클래스를 인식합니다 +++
num_classes = len(train_generator.class_indices)
print(f"총 {num_classes}개의 클래스를 학습합니다:")
print(train_generator.class_indices) 
# {'0_boredom': 0, '1_drowsy': 1, '2_neutral': 2} 로 출력되는지 확인!

# --- 3. 모델 구축 (CNN) ---
# (이전과 동일한 검증된 모델 구조)
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 1)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten()) 
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# +++ num_classes는 3이 됩니다 +++
model.add(Dense(num_classes, activation='softmax')) 

model.summary()

# --- 4. 모델 컴파일 및 콜백 설정 ---
model.compile(
    # +++ 표준 학습률(0.001)로 복귀 +++
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# +++ 새 모델 파일명으로 저장 +++
model_checkpoint = ModelCheckpoint(
    filepath='emotion_model_3class.h5', 
    monitor='val_accuracy', # 검증 정확도를 기준으로
    save_best_only=True,    # 가장 좋은 모델만 저장
    verbose=1
)
early_stopping = EarlyStopping(
    monitor='val_loss', # 검증 손실을 기준으로
    patience=10,        # 10 에포크 동안 개선(손실 감소)이 없으면 중단
    restore_best_weights=True # 가장 좋았던 시점의 가중치로 복원
)

# --- 5. 모델 학습 ---
print("\n--- 3-Class (Boredom, Drowsy, Neutral) 모델 학습을 시작합니다 ---")

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[model_checkpoint, early_stopping]
    # +++ class_weight는 사용하지 않습니다 (데이터가 균형 잡혔기를 기대) +++
)

print("\n--- 모델 학습 완료 ---")
print("가장 성능이 좋은 모델이 'emotion_model_3class.h5'로 저장되었습니다.")