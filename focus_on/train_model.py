# 파일명: train_model.py
# (DAiSEE 4-Class 학습용)

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
EPOCHS = 100 

# +++ 수정: 1단계에서 생성한 폴더 경로로 변경 +++
base_dir = './dataset_daisee_4class' 
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# (이하 코드는 동일합니다)
# --- 2. 데이터 준비 ---
train_datagen = ImageDataGenerator(
    rescale=1./255, rotation_range=30,
    width_shift_range=0.2, height_shift_range=0.2,
    shear_range=0.2, zoom_range=0.2,
    horizontal_flip=True, fill_mode='nearest'
)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical',
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

num_classes = len(train_generator.class_indices)
print(f"총 {num_classes}개의 클래스를 학습합니다:")
print(train_generator.class_indices) # {'0_boredom': 0, '1_engagement': 1, ...}

# --- 3. 모델 구축 ---
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
model.add(Dense(num_classes, activation='softmax')) 

model.summary()

# --- 4. 모델 컴파일 및 콜백 설정 ---
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model_checkpoint = ModelCheckpoint(
    filepath='emotion_model_daisee_4class.h5', # (모델 이름 변경)
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

# --- 5. 모델 학습 ---
print("\n--- DAiSEE 4-Class 모델 학습을 시작합니다 ---")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[model_checkpoint, early_stopping]
)
print("\n--- 모델 학습 완료 ---")
print("가장 성능이 좋은 모델이 'emotion_model_daisee_4class.h5'로 저장되었습니다.")