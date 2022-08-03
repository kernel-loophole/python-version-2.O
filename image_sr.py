#image reconition using tensorflow
import tensorflow as tf
import numpy as np
from PIL import Image
form tensorflow.keras.preprocessing import image


def read_data_set(path):
    data_set = []
    for i in range(1, 6):
        img_path = path + str(i) + ".jpg"
        img = preprocess_image(img_path)
        data_set.append(img)
    return data_set


def convert_image_to_array(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)
    return img_array
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    return img_array


def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    return img_array
def load_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    return img_array
def load_model():
    model = tf.keras.models.load_model('model.h5')
    return model
def predict(model, image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    return prediction
def get_prediction(prediction):
    prediction = prediction.argmax()
    return prediction
def get_prediction_name(prediction):
    prediction_name = ""
    if prediction == 0:
        prediction_name = "A"
    elif prediction == 1:
        prediction_name = "B"
    elif prediction == 2:
        prediction_name = "C"
    elif prediction == 3:
        prediction_name = "D"
    elif prediction == 4:
        prediction_name = "E"
def main():
    model = load_model()
    image_path = "test.jpg"
    prediction = predict(model, image_path)
    prediction = get_prediction(prediction)
    prediction_name = get_prediction_name(prediction)
    print(prediction_name)
    