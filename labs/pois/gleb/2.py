import os
import keras
import tensorflow as tf
from keras.src.layers import Flatten, Dense
from sklearn.datasets import load_digits
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Загрузка данных
data = load_digits()

plt.gray()
X = data.images

Y = data.target
# Создание модели
model = tf.keras.Sequential([

    Flatten(input_shape=(8, 8, 1)),

    Dense(128, activation='relu'),

    Dense(10, activation='softmax')

])
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.33, random_state=42)
# print(model.summary())
X_train = X_train / 255
# print(np.shape(X_train))
X_test = X_test / 255
y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)
model.compile(optimizer='adam',

              loss='categorical_crossentropy',

              metrics=['accuracy'])

model.fit(X_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2)
model.evaluate(X_test, y_test_cat)
n = 1

x = np.expand_dims(X_test[n], axis=0)

res = model.predict(x)
# print(np.argmax(res))
# plt.imshow(X_test[n], cmap = plt.cm.binary)
# plt.show()

# Работа модели на тесте
pred = model.predict(X_test)
pred = np.argmax(pred, axis=1)

# print(pred.shape)

# print(pred[:20])
# print(y_test[:20])

# Маска для определения ошибочных решений
mask = pred == y_test
# print(mask[:10])

x_false = X_test[~mask]
y_false = y_test[~mask]
false_pred = pred[~mask]
# print(x_false.shape)


# Вывод результатов
plt.figure(figsize=(10, 5))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(x_false[i], cmap=plt.cm.binary)
    print("Predicted:" + str(false_pred[i]) + " , actual: " + str(y_false[i]))
print("Correct answers: " + str(len(pred) - len(false_pred)) + "/" + str(len(pred)))
plt.show()
