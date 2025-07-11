from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os
import streamlit as st

# Get the absolute path to the directory the script is in
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths to the files
model_path = os.path.join(base_dir, "keras_model.h5")
labels_path = os.path.join(base_dir, "labels.txt")

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(model_path, compile=False)

# Load the labels
class_names = open(labels_path, "r").readlines()

def classify(image_path):
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    return class_name[2:], confidence_score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)


def app():
    st.set_page_config(
        page_title="Ex-stream-ly Cool App",
        page_icon="🚗"
    )
    st.header("Distracted Driver App", divider="gray")
    st.markdown("Project by Daivien, Anish, Sienna, Chad, Harris, Angelina, Yusef")

    picture = st.camera_input("Take a picture")
    if picture:
        label, score = classify(picture)
        st.markdown(f"Label: {label}")
        st.markdown(f"Model Confidence: {score}")

if __name__ == "__main__":
    app()
