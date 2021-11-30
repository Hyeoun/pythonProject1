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
imgs = []
for i in Numbers:
    i = int(i)
    z = np.random.normal(0, 1, (1, 100))
    fake_imgs = number_GAN_models[i].predict(z)
    fake_imgs = 0.5 * fake_imgs + 0.5
    imgs.append(fake_imgs.reshape(28, 28))
    print(fake_imgs.shape)

img = imgs[0]
for i in range(1,4):
    img = np.append(img, imgs[i], axis=1)

print(img.shape)
plt.cool() # gray, cool, hot, spring, summer, autumn, winter, bone, copper, magma, pink, prism, plasma
plt.imshow(img)
plt.axis('off')
plt.show()