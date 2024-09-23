import os
from sklearn.datasets import load_digits
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2
import keras
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from keras.src.layers import Dense, Conv1D, MaxPooling1D, Flatten


def F_to_C(c: np.array, f: np.array):
    """Метод для перевода из Фаренгейта в градусы Цельсия (задание 1)"""

    # однослойная сеть
    model = keras.Sequential()
    model.add(Dense(units=1, input_shape=(1,), activation='linear'))
    model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.1))
    log = model.fit(c, f, epochs=1000, verbose=False)
    pred = model.predict(x=np.array([100]))
    print(pred)

    # двухслойная сеть
    model.layers.pop()
    model.add(Dense(units=6, input_shape=(1,), activation='linear'))
    model.add(Dense(units=1, activation='linear'))
    pred = model.predict(x=np.array([100]))
    print(pred)


def num_detection():
    """Метод для обучения и применения нейронной сети, распознающей числа"""

    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    # датасет из sklearn
    data = load_digits()
    plt.gray()
    X = data.images
    Y = data.target

    # обучаем модель
    model = tf.keras.Sequential([Flatten(input_shape=(8, 8, 1)), Dense(128, activation='relu'),
                                 Dense(10, activation='softmax')])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    X_train = X_train / 255
    X_test = X_test / 255
    y_train_cat = keras.utils.to_categorical(y_train, 10)
    y_test_cat = keras.utils.to_categorical(y_test, 10)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2)
    model.evaluate(X_test, y_test_cat)
    n = 1
    x = np.expand_dims(X_test[n], axis=0)

    # применяем модель на тестовой подвыборке
    pred = model.predict(X_test)
    pred = np.argmax(pred, axis=1)
    mask = pred == y_test
    x_false = X_test[~mask]
    y_false = y_test[~mask]
    false_pred = pred[~mask]

    plt.figure(figsize=(10, 5))
    for i in range(25):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(x_false[i], cmap=plt.cm.binary)
    print("Статистика верных ответов: " + str(len(pred) - len(false_pred)) + "/" + str(len(pred)))
    plt.show()


def predict_csv(data):
    Y = data['y']
    X = data.drop(data.columns[6], axis=1)
    X = X.to_numpy()
    Y = Y.to_numpy()

    # делим выборку на тест и трейн
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)

    # создаем слои модели с содержанием следующих слоев сети:
    # сверточный, max-pulling, сверточный, max-pooling, сверточный, выравнивающий, полносвязный, вызодной полносвязный
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
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['r2_score'])

    # Обучаем модель
    model.fit(X_train, y_train, batch_size=32, epochs=30, validation_split=0.2)

    # результаты
    print(model.evaluate(X_test, y_test))
    res = model.predict(X)
    np.savetxt('output.csv', res)


def style_pass(img, img_style):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(img_style)
    plt.show()

    x_img = keras.applications.vgg19.preprocess_input(np.expand_dims(img, axis=0))
    x_style = keras.applications.vgg19.preprocess_input(np.expand_dims(img_style, axis=0))

    def deprocess_img(processed_img):
        x = processed_img.copy()
        if len(x.shape) == 4:
            x = np.squeeze(x, 0)
        assert len(x.shape) == 3, ("Input to deprocess image must be an image of "
                                   "dimension [1, height, width, channel] or [height, width, channel]")
        if len(x.shape) != 3:
            raise ValueError("Invalid input to deprocessing image")

        x[:, :, 0] += 103.939
        x[:, :, 1] += 116.779
        x[:, :, 2] += 123.68
        x = x[:, :, ::-1]
        x = np.clip(x, 0, 255).astype('uint8')
        return x

    vgg = keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False
    content_layers = ['block5_conv2']
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

    num_content_layers = len(content_layers)
    num_style_layers = len(style_layers)
    style_outputs = [vgg.get_layer(name).output for name in style_layers]
    content_outputs = [vgg.get_layer(name).output for name in content_layers]
    model_outputs = style_outputs + content_outputs

    model = keras.models.Model(vgg.input, model_outputs)
    for layer in model.layers:
        layer.trainable = False

    def get_feature_representations(model):
        style_outputs = model(x_style)
        content_outputs = model(x_img)

        style_features = [style_layer[0] for style_layer in style_outputs[:num_style_layers]]
        content_features = [content_layer[0] for content_layer in content_outputs[num_style_layers:]]
        return style_features, content_features

    def get_content_loss(base_content, target):
        return tf.reduce_mean(tf.square(base_content - target))

    def gram_matrix(input_tensor):
        channels = int(input_tensor.shape[-1])
        a = tf.reshape(input_tensor, [-1, channels])
        n = tf.shape(a)[0]
        gram = tf.matmul(a, a, transpose_a=True)
        return gram / tf.cast(n, tf.float32)

    def get_style_loss(base_style, gram_target):
        gram_style = gram_matrix(base_style)

        return tf.reduce_mean(tf.square(gram_style - gram_target))

    def compute_loss(model, loss_weights, init_image, gram_style_features, content_features):
        style_weight, content_weight = loss_weights

        model_outputs = model(init_image)

        style_output_features = model_outputs[:num_style_layers]
        content_output_features = model_outputs[num_style_layers:]

        style_score = 0
        content_score = 0

        weight_per_style_layer = 1.0 / float(num_style_layers)
        for target_style, comb_style in zip(gram_style_features, style_output_features):
            style_score += weight_per_style_layer * get_style_loss(comb_style[0], target_style)

        weight_per_content_layer = 1.0 / float(num_content_layers)
        for target_content, comb_content in zip(content_features, content_output_features):
            content_score += weight_per_content_layer * get_content_loss(comb_content[0], target_content)

        style_score *= style_weight
        content_score *= content_weight

        loss = style_score + content_score
        return loss, style_score, content_score

    num_iterations = 100
    content_weight = 1e3
    style_weight = 1e-2

    style_features, content_features = get_feature_representations(model)
    gram_style_features = [gram_matrix(style_feature) for style_feature in style_features]

    init_image = np.copy(x_img)
    init_image = tf.Variable(init_image, dtype=tf.float32)

    opt = tf.compat.v1.train.AdamOptimizer(learning_rate=2, beta1=0.99, epsilon=1e-1)
    iter_count = 1
    best_loss, best_img = float('inf'), None
    loss_weights = (style_weight, content_weight)

    cfg = {
        'model': model,
        'loss_weights': loss_weights,
        'init_image': init_image,
        'gram_style_features': gram_style_features,
        'content_features': content_features
    }

    norm_means = np.array([103.939, 116.779, 123.68])
    min_vals = -norm_means
    max_vals = 255 - norm_means
    imgs = []

    for i in range(num_iterations):
        with tf.GradientTape() as tape:
            all_loss = compute_loss(**cfg)

        loss, style_score, content_score = all_loss
        grads = tape.gradient(loss, init_image)

        opt.apply_gradients([(grads, init_image)])
        clipped = tf.clip_by_value(init_image, min_vals, max_vals)
        init_image.assign(clipped)

        if loss < best_loss:
            best_loss = loss
            best_img = deprocess_img(init_image.numpy())

            plot_img = deprocess_img(init_image.numpy())
            imgs.append(plot_img)

    plt.imshow(best_img)
    # print(best_loss)

    image = Image.fromarray(best_img.astype('uint8'), 'RGB')
    image.save("result2.jpg")


def main():
    # задание 1
    c = np.array([-40, -10, 0, 8, 15, 22, 38])
    f = np.array([-40, 14, 32, 46, 59, 72, 100])
    F_to_C(c, f)

    # задание 2
    num_detection()

    # задание 3
    data = pd.read_csv("raw_data5.csv")
    predict_csv(data)

    # задание 4
    img = cv2.imread('belka.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_style = cv2.imread('davinci.jpg')
    img_style = cv2.cvtColor(img_style, cv2.COLOR_BGR2RGB)
    style_pass(img, img_style)


if __name__ == '__main__':
    main()
