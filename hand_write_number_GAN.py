import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import load_model

# model = load_model('./models/generator_mnist_5.h5')
# model.summary()
# exit()

number_GAN_models = []
for i in range(10):
    try: number_GAN_models.append(load_model('./models/generator_mnist_{}.h5'.format(i)))
    except: number_GAN_models.append(load_model('./models/generator_mnist_0.h5'.format(i)))

four_digit_number = '0187'
Numbers = list(four_digit_number)
print(Numbers)
img = []
for i in Numbers:
    i = int(i)
    z = np.random.normal(0, 1, (4 * 4, 100))
    fake_imgs = number_GAN_models[i].predict(z)
    fake_imgs = 0.5 * fake_imgs + 0.5
    img.append(fake_imgs)
    print(fake_imgs.shape)

_, axs = plt.subplots(1, 4, figsize=(4, 4), sharey=True, sharex=True)
cnt = 0

for j in range(4):
    axs[j].imshow(img[j][cnt, :, :], cmap='gray')
    axs[j].axis('off')
    cnt += 1
plt.show()