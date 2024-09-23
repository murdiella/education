import pandas as pd
import keras

from sklearn.model_selection import train_test_split
import numpy as np
from keras.src.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout

# Подготавливаем данные
data = pd.read_csv("raw_data5.csv")
Y = data['y']
X = data.drop(data.columns[6], axis=1)
X = X.to_numpy()
Y = Y.to_numpy()
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.33, random_state=42)
X_train = np.expand_dims(X_train, axis=2)
X_test = np.expand_dims(X_test, axis=2)
print(np.shape(X_train))
# Создаем модель
model = keras.Sequential()
model.add(Conv1D(32, 6, input_shape=(6, 1,), padding='same', activation='linear'))
model.add(MaxPooling1D(3, strides=2))
model.add(Conv1D(128, 3, input_shape=(6, 1,), padding='same', activation='linear'))
model.add(MaxPooling1D(2, strides=2))
model.add(Conv1D(256, 1, input_shape=(6, 1,), padding='same', activation='linear'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1))
model.summary()
model.compile(optimizer='adam',

              loss='mean_squared_error',
              metrics=['r2_score'])

# Обучаем модель
model.fit(X_train, y_train, batch_size=32, epochs=30, validation_split=0.2)

print(model.evaluate(X_test, y_test))
res = model.predict(X)
np.savetxt('output.csv', res)
