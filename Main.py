import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ds_train = tf.keras.utils.image_dataset_from_directory(
    directory = '/kaggle/input/dogs-vs-cats/train',
    labels='inferred',
    label_mode='int',
    color_mode='rgb',
    batch_size=32,
    image_size=(256, 256),
)


ds_valid = tf.keras.utils.image_dataset_from_directory(
    directory = '/kaggle/input/dogs-vs-cats/test',
    labels='inferred',
    label_mode='int',
    color_mode='rgb',
    batch_size=32,
    image_size=(256, 256),
)


#Normalization
def preprocessing_imgs(img, label):
    image = tf.cast(img/255.,tf.float32)
    return img, label
ds_train = ds_train.map(preprocessing_imgs)
ds_valid = ds_valid.map(preprocessing_imgs)



model1 = tf.keras.Sequential()

model1.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu', input_shape=(256,256,3)))
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Flatten())

model1.add(Dense(128,activation='relu'))
model1.add(Dense(64,activation='relu'))
model1.add(Dense(1,activation='sigmoid'))


model1.summary()

model1.compile(optimizer='adam',loss='binary_crossentropy',metrics =['accuracy'])
history = model1.fit(ds_train,epochs=10,validation_data=ds_valid)


plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()


import cv2
teh1 = cv2.imread('/kaggle/input/dogs-vs-cats/test/cats/cat.10188.jpg')
plt.imshow(teh1)


print(teh1.shape)
teh1 = cv2.resize(teh1,(256,256)) #Resizing to 256x256
teh1_in = teh1.reshape((1,256,256,3))


out1 = model1.predict(teh1_in)
print(out1)
if out1>0.5:
    print("It's a dog!")
else:
    print("It's a cat!")
