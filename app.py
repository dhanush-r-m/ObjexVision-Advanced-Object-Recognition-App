import os
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from tensorflow.keras.utils import img_to_array, load_img
import tensorflow as tf
import requests
import time
import streamlit_lottie as st_lottie

# Disable oneDNN custom operations warning
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Streamlit page configuration
st.set_page_config(page_title="CIFAR-10 Image Classification", page_icon="🖼️", layout="wide")

# Load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie Animation
lottie_url = "https://lottie.host/de06d967-8825-499e-aa8c-a88dd15e1a08/dH2OtlPb3c.json"
lottie_animation = load_lottie_url(lottie_url)

# Sidebar with unique elements
with st.sidebar:
    st_lottie.st_lottie(lottie_animation, height=200, width=200, key="lottie_animation")
    st.markdown("<h2 style='color: #007bff;'>Explore the App!</h2>", unsafe_allow_html=True)
    st.markdown("**About the Model:** This CIFAR-10 classifier uses a convolutional neural network trained on thousands of images.")
    
    # Features section with hover effect
    st.markdown(""" 
        <style>
            .feature-hover {
                position: relative;
                display: inline-block;
                color: #007bff;
                cursor: pointer;
            }

            .feature-hover .tooltip-text {
                visibility: hidden;
                width: 200px;
                background-color: #333;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 100%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            }

            .feature-hover:hover .tooltip-text {
                visibility: visible;
                opacity: 1;
            }
        </style>

        <ul>
            <li>
                <div class="feature-hover">Fast Classification(Cool)
                    <span class="tooltip-text">Get predictions in seconds.Enjoy a sleek and modern design.</span>
                </div>
            </li>
            <li>
                <div class="feature-hover">Highly Accurate
                    <span class="tooltip-text">Model accuracy is up to 92%.</span>
                </div>
            </li>
        </ul>
    """, unsafe_allow_html=True)
    # ✅ Developer tag with GitHub icon and link
    st.markdown("""
        <hr style="border: 1px solid #007bff;">
        <div style="text-align:center">
            <h4>👨‍💻 Developer: Dhanush Moolemane</h4>
            <a href="https://github.com/dhanush-r-m" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="30" height="30">
            </a>
        </div>
    """, unsafe_allow_html=True)

# CIFAR-10 class names
class_names = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

# Load model
@st.cache_resource
def load_my_model():
    model = tf.keras.models.load_model("final_model1.h5")
    # Compile the model (use the optimizer and loss you trained with)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

model = load_my_model()

# Main title with cool text effect
st.markdown(""" 
    <h1 style="text-align:center; color: #007bff; font-family: 'Courier New', Courier, monospace; animation: glow 2s ease-in-out infinite alternate;">
    🖼️ CIFAR-10 Image Classification
    </h1>
    <style>
    @keyframes glow {
        0% {
            text-shadow: 0 0 10px #9b59b6, 0 0 20px #007bff, 0 0 30px #007bff, 0 0 40px #9b59b6;
        }
        100% {
            text-shadow: 0 0 20px #8e44ad, 0 0 30px #007bff, 0 0 40px #007bff, 0 0 50px #8e44ad;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.header("Upload an image and get predictions!")

# Image loading function
def load_image(filename):
    img = load_img(filename, target_size=(32, 32))
    img = img_to_array(img)
    img = img.reshape(1, 32, 32, 3)
    img = img.astype('float32')
    img = img / 255.0
    return img

# Create folder for images if not exist
if not os.path.exists('./images'):
    os.makedirs('./images')

# Upload image section with fancy file uploader
image_file = st.file_uploader("🌄 Upload an image", type=["jpg", "png"], key="file_uploader")

if image_file is not None:
    if st.button("Classify Image 🧠", key="classify_button"):
        img_path = f"./images/{image_file.name}"
        with open(img_path, "wb") as f:
            f.write(image_file.getbuffer())
        
        image = Image.open(img_path)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        img_to_predict = load_image(img_path)

        # Progress spinner
        with st.spinner('🔍 Classifying image...'):
            time.sleep(2)
            predictions = model.predict(img_to_predict)
            predicted_class = np.argmax(predictions, axis=-1)
            confidence = np.max(predictions)

        # Threshold and result display
        confidence_threshold = 0.60  # Increased confidence threshold to 60%

        if confidence < confidence_threshold:
            result = f"Prediction: Not a CIFAR-10 class (Confidence: {confidence*100:.2f}%)"
        else:
            result = f"Prediction: {class_names[predicted_class[0]]} with {confidence*100:.2f}% confidence"

        st.success(result)

        os.remove(img_path)

# Add unique progress bar for better interactivity
if st.button("Reload App"):
    st.progress(100)

# Additional CIFAR-10 Information
st.markdown(""" 
### **CIFAR-10 Classes**:
- <span title="✈️ Aircraft used in transportation and travel.">**airplane**</span>
- <span title="🚗 Motor vehicles designed for roads.">**automobile**</span>
- <span title="🐦 Creatures from the bird species.">**bird**</span>
- <span title="🐱 Domesticated feline pets.">**cat**</span>
- <span title="🦌 Animals that belong to the deer family.">**deer**</span>
- <span title="🐶 Domesticated dogs.">**dog**</span>
- <span title="🐸 Amphibians with moist skin.">**frog**</span>
- <span title="🐴 Domesticated or wild horses.">**horse**</span>
- <span title="🚢 Sea-going vessels used for transport.">**ship**</span>
- <span title="🚚 Large vehicles used for goods transport.">**truck**</span>
""", unsafe_allow_html=True)

# Data for CIFAR-10 performance
data = {
    "Class": class_names,
    "Accuracy": [0.89, 0.85, 0.78, 0.92, 0.80, 0.76, 0.83, 0.88, 0.90, 0.81],
    "Precision": [0.87, 0.82, 0.77, 0.91, 0.79, 0.75, 0.81, 0.87, 0.88, 0.80],
}

performance_df = pd.DataFrame(data)
st.write(performance_df)

