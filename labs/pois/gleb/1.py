import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.src.layers import Flatten, Dense
c = np.array([-40, -10, 0, 8, 15, 22, 38])
f = np.array([-40, 14, 32, 46, 59, 72, 100])
model = keras.Sequential()
model.add(Dense(units=1, input_shape=(1,), activation='linear'))
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.1))

log = model.fit(c, f, epochs=1000, verbose=False)
#plt.plot(log.history['loss'])
#plt.grid(True)
#plt.show()

pred = model.predict(x=np.array([100]))
print(pred)
model.layers.pop()
model.add(Dense(units=6, input_shape=(1,), activation='linear'))
model.add(Dense(units=1, activation='linear'))

pred = model.predict(x=np.array([100]))
print(pred)
#print(model.get_weights())
