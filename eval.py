#!/usr/bin/env python3
import numpy as np
from keras.models import load_model
from sklearn.metrics import classification_report

def load_data():
    x_te = []
    y_te = []

    test_i = 3
    datas = np.load('feature/test_%s.npy' % test_i)
    for data in datas:
        x_te.append(data.get('x'))
        y_te.append(data.get('y'))

    x_te = np.array(x_te)
    y_te = np.array(y_te)
    print(x_te.shape, y_te.shape)

    return x_te, y_te


if __name__ == '__main__':
    model_path = 'models/lang_classify.h5'

    x_true, y_true = load_data()
    model = load_model(model_path)
    y_pred = np.argmax(model.predict(x_true), axis=1)
    print(classification_report(y_true, y_pred))
