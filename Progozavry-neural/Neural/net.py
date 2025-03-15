#подключение библиотеки keras
import keras
#последовательная модель
from keras.models import Sequential
#слои dense(слой с плотными связями),
#conv2d (2d слой свертки), 
#maxpool2d (максимальная операция объединения для 2d пространственных данных),
#flatten(сглаживание),
#dropout(для отсева данных).
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
#оптимизаторы
#Adam - метод стохастического градиентного спуска
#RMSprop - поддержание среднего квадрата градиентов 
#для деления градиента на корень среднего значения
#Adagrad - оптмизатор с адаптивной скоростью обучения 
from keras.optimizers import Adam, RMSprop, Adagrad
#слой для нормализации входных данных
from keras.layers import BatchNormalization
#подключение библиотеки scikit-learn 
#classification_report для создания текстового отчета, который
#показывает основные показатели классификации
#confusion_matrix для вычисления оценки точности классификации
from sklearn.metrics import classification_report, confusion_matrix
#подключение библиотеки tensorflow
import tensorflow as tf
#подключение библиотеки numpy для числовых операций
import numpy as np
import sys
sys.path.insert(1, '../Progozavry/')
from Neural.dataset import Dataset

class Network:
    def __init__(self, size) -> None:
        self.size = size
        self.labels = ['No apnoe', 'Apnoe']#'Light apnoe', 'Hard apnoe']
        self.model = Sequential()
        #добавление сверточного слоя с 64 фильтрами, размером ядра 3х3, функцией активации ReLU,
        #padding="same" означает, что выход имеет тот же размер, что и вход
        #input_shape устанавливает размерность входных данных
        self.model.add(Conv2D(64,3,padding="same", activation="relu", input_shape = (512, 512, 1)))
        #добавление слоя объединения двумерных пространственных данных для уменьшения размерности данных
        self.model.add(MaxPool2D())
        #добавление сверточного слоя с 64 фильтрами, размером ядра 3х3, функцией активации ReLU,
        #padding="same" означает, что выход имеет тот же размер, что и вход
        self.model.add(Conv2D(64, 3, padding="same", activation="relu"))
        #добавление слоя объединения двумерных пространственных данных для уменьшения размерности данных
        self.model.add(MaxPool2D())
        #добавление сверточного слоя с 128 фильтрами, размером ядра 3х3, функцией активации ReLU,
        #padding="same" означает, что выход имеет тот же размер, что и вход
        self.model.add(Conv2D(128, 3, padding="same", activation="relu"))
        #добавление слоя объединения двумерных пространственных данных для уменьшения размерности данных
        self.model.add(MaxPool2D())
        #добавление слоя Flatten для преобразования данных в одномерный массив
        self.model.add(Flatten())
        #добавление полносвязного слоя с 256 нейронами и функцией активации ReLU
        self.model.add(Dense(256,activation="relu"))
        #применение отсева входных данных для предотвращения переобучения
        self.model.add(Dropout(0.5))
        #добавление слоя BatchNormalization для нормализации данных
        self.model.add(BatchNormalization())
        #добавления полносвязного слоя с 2 выходными нейронами и функцией активации softmax для классификации
        self.model.add(Dense(len(self.labels), activation="softmax"))
        #вывод структуры модели
        self.model.summary()
        #создание оптимизатора Adam с заданной скоростью обучения (learning rate)
        self.opt = Adam(learning_rate=1e-5)
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer=self.opt, metrics=["accuracy"])

    def loadWeights(self, filename):
        self.model.load_weights(filename)

    def saveWeights(self, filename):
        self.model.save_weights(filename)

    def train(self, dataset, epochs):
        history = self.model.fit(dataset.train[0], dataset.train[1], epochs = epochs,
            batch_size = len(dataset.train[0]) // 2, validation_split = 0.25, verbose=1)
        print('Model train completed')
        #print(history.history.keys())