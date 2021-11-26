import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential

OUT_DIR = './OUT_img'
img_shape = (28, 28, 1)
epoch = 100000
batch_size = 128
noise = 100
sample_interval = 100

(X_train, _), (_, _) = mnist.load_data()
print(X_train.shape)

X_train = X_train / (255 / 2) - 1  # 정규화
X_train = np.expand_dims(X_train, axis=3)  # 이미지 2차원을 3차원으로 늘린다.
print(X_train.shape)

generator_model = Sequential()  # 이미지 생성모델
generator_model.add(Dense(128, input_dim=noise))
generator_model.add(LeakyReLU(alpha=0.01))
generator_model.add(Dense(784, activation='tanh'))
generator_model.add(Reshape(img_shape))
generator_model.summary()

lrelu = LeakyReLU(alpha=0.01)
discriminator_model = Sequential()  # 이미지 판별 모델
discriminator_model.add(Flatten(input_shape=img_shape))
discriminator_model.add(Dense(128, activation=lrelu))
discriminator_model.add(Dense(1, activation='sigmoid'))
discriminator_model.summary()

discriminator_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
discriminator_model.trainable = False  # 학습 안되게 막아놓는다.

gan_model = Sequential()
gan_model.add(generator_model)
gan_model.add(discriminator_model)
gan_model.summary()
gan_model.compile(loss='binary_crossentropy', optimizer='adam')

real = np.ones((batch_size, 1))  # 배치사이즈만큼 1로 채워진 라벨을 만든다.
print(real)
fake = np.zeros((batch_size, 1))  # 배치사이즈만큼 0으로 채워진 라벨을 만든다.
print(fake)

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