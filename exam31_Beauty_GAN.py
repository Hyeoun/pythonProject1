import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

detector = dlib.get_frontal_face_detector()
shape = dlib.shape_predictor('./models/shape_predictor_5_face_landmarks.dat')

img = dlib.load_rgb_image('./imgs/03.jpg')
plt.figure(figsize=(16, 10))
plt.imshow(img)
plt.show()

img_result = img.copy()
dets = detector(img, 1)

if len(dets) == 0:
    print('Not find faces')

fig, ax = plt.subplots(1, figsize=(16, 10))

for det in dets:
    x, y, w, h = det.left(), det.top(), det.width(), det.height()
    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='b', facecolor='none')
    ax.add_patch(rect)

ax.imshow(img_result)
plt.show()