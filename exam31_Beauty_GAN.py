import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

detector = dlib.get_frontal_face_detector()
Shape = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

img = dlib.load_rgb_image('./imgs/13.jpg')
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

fig, ax = plt.subplots(1, figsize=(16, 10))
obj = dlib.full_object_detections()

for detection in dets:
    s = Shape(img, detection)
    obj.append(s)

    for point in s.parts():
        circle = patches.Circle((point.x, point.y), radius=2, edgecolor='b', facecolor='b')
        ax.add_patch(circle)
    ax.imshow(img_result)
plt.show()

# 얼굴 위치 맞추기

def align_faces(img):
    dets = detector(img, 1)
    objs = dlib.full_object_detections()  # 얼굴 찾아주는 함수
    for detection in dets:
        s = Shape(img, detection)
        objs.append(s)
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)  # padding : 얼굴만 나오지 않게 여유를 준다.
    return faces

# test
test_img = dlib.load_rgb_image('./imgs/13.jpg')
test_faces = align_faces(test_img)
fig, axes = plt.subplots(1, len(test_faces)+1, figsize=(20, 16))
axes[0].imshow(test_img)

for i, face in enumerate(test_faces):
    axes[i + 1].imshow(face)
plt.show()

sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.import_meta_graph('./models/model.meta')
graph = tf.get_default_graph()
X = graph.get_tensor_by_name('X:0')
Y = graph.get_tensor_by_name('Y:0')
Xs = graph.get_tensor_by_name('generator/xs:0')

def preprocess(img):  # 전처리
    return img / (255 / 2) - 1
def deprecess(img):  # 이미지 복원
    return (img + 1) / 2

img1 = dlib.load_rgb_image('./imgs/12.jpg')
img1_faces = align_faces(img1)

img2 = dlib.load_rgb_image('./imgs/makeup/XMY-266.png')
img2_faces = align_faces(img2)

fig, axes = plt.subplots(1, 2, figsize=(16, 10))
axes[0].imshow(img1_faces[0])
axes[1].imshow(img2_faces[0])
plt.show()
