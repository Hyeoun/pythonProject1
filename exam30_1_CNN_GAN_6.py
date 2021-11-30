import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
from tensorflow.keras import datasets
import pandas as pd

My_number = 6
OUT_DIR = './CNN_OUT_{}_img'.format(My_number)
if not os.path.exists(OUT_DIR):  # 원하는 폴더가 없으면 생성한다.
    os.makedirs(OUT_DIR)
img_shape = (28, 28, 1)
epoch = 10000
batch_size = 128
noise = 100
sample_interval = 100

# build generator
generator_model = Sequential()
generator_model.add(Dense((256*7*7), input_dim=noise))
generator_model.add(Reshape((7, 7, 256)))  # 7 * 7 사이즈 256개 생성
generator_model.add(Conv2DTranspose(128, kernel_size=3, strides=2, padding='same'))  # 이미지 여러장 받아서 128장으로 줄인다. / strides : 커널 적용시 몇칸 뛸지 결정
generator_model.add(BatchNormalization())  # == 업샘플링
generator_model.add(LeakyReLU(alpha=0.01))
generator_model.add(Conv2DTranspose(64, kernel_size=3, strides=1, padding='same'))  # 사이즈를 늘리지 않음
generator_model.add(BatchNormalization())
generator_model.add(LeakyReLU(alpha=0.01))
generator_model.add(Conv2DTranspose(1, kernel_size=3, strides=2, padding='same'))  # 최종적으로 1장으로 줄어든다.
generator_model.add(Activation('tanh'))
generator_model.summary()

# build discriminator
discriminator_model = Sequential()
discriminator_model.add(Conv2D(32, kernel_size=3, strides=2, padding='same', input_shape=img_shape))
# generator_model.add(BatchNormalization())
discriminator_model.add(LeakyReLU(alpha=0.01))
discriminator_model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
# generator_model.add(BatchNormalization())
discriminator_model.add(LeakyReLU(alpha=0.01))
discriminator_model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
# generator_model.add(BatchNormalization())
discriminator_model.add(LeakyReLU(alpha=0.01))
discriminator_model.add(Flatten())
discriminator_model.add(Dense(1, activation='sigmoid'))
discriminator_model.summary()

discriminator_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
discriminator_model.trainable = False

# build GAN
gan_model = Sequential()
gan_model.add(generator_model)
gan_model.add(discriminator_model)
print(gan_model.summary())
gan_model.compile(loss='binary_crossentropy', optimizer='adam')

(X_train, Y_train), (_, _) = mnist.load_data()
print(X_train.shape, Y_train.shape)
X_train = X_train[Y_train == My_number]
print(len(X_train))

_, axs = plt.subplots(4, 4, figsize=(4, 4),
            sharey=True, sharex=True)
cnt = 0
for i in range(4):
    for j in range(4):
        axs[i, j].imshow(X_train[cnt, :, :], cmap='gray')
        axs[i, j].axis('off')
        cnt += 1
plt.show()

X_train = X_train / (255 / 2) - 1
X_train = np.expand_dims(X_train, axis=3)
print(X_train.shape)

real = np.ones((batch_size, 1))
fake = np.zeros((batch_size, 1))

for itr in range(epoch):
    idx = np.random.randint(0, X_train.shape[0], batch_size)  # X_train.shape[0] = X_train의 개수
    real_imgs = X_train[idx]  # 리얼 이미지 6만장중 배치사이즈만큼 랜덤하게 뽑는다.

    z = np.random.normal(0, 1, (batch_size, noise))  # 평균이 0, 표준편차가 1인 노이즈 생성
    fake_imgs = generator_model.predict(z)  # 배치 사이즈 만큼의 잡음 이미지 생성

    d_hist_real = discriminator_model.train_on_batch(real_imgs, real)  # train_on_batch = 학습
    d_hist_fake = discriminator_model.train_on_batch(fake_imgs, fake)  # 진짜와 가짜를 넣고 구분할수 있도록 학습

    d_loss, d_acc = 0.5 * np.add(d_hist_real, d_hist_fake)  # 각각 학습했을때의 로스값과 어큐러시값을 더해서 평균 저장
    discriminator_model.trainable = False  # 학습 정지

    z = np.random.normal(0, 1, (batch_size, noise))
    gan_hist = gan_model.train_on_batch(z, real)  # z = 가짜 이미지, real = 진짜
    # gan_model이 z를 real이 될 수 있도록 학습

    if itr % sample_interval == 0:  # 학습 과정 확인
        print('%d [D loss: %f, acc.: %.2f%%] [G loss: %f]' %(itr, d_loss, d_acc * 100, gan_hist))
        row = col = 4
        z = np.random.normal(0, 1, (row * col, noise))  # 잡음 16개
        fake_imgs = generator_model.predict(z)
        fake_imgs = 0.5 * fake_imgs + 0.5  # 이미지 복원
        _, axs = plt.subplots(row, col, figsize=(row, col), sharey=True, sharex=True)  # 16개 이미지에 x,y값을 공유한다.

        cnt = 0
        for i in range(row):
            for j in range(col):
                axs[i, j].imshow(fake_imgs[cnt, :, :, 0], cmap='gray')
                axs[i, j].axis('off')
                cnt += 1
        path = os.path.join(OUT_DIR, 'img-{}'.format(itr + 1))
        plt.savefig(path)
        plt.close()

generator_model.save('./generator_mnist_{}.h5'.format(My_number))