import os
import shutil
import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO

MODEL_PATH = "best.pt"
OUTPUT_DIR = "categorized_images"

CATEGORIES = {
    "Plastic": [
        "plastic_bag", "plastic_bottle", "plastic_bottle_cap", "plastic_box",
        "plastic_cultery", "plastic_cup", "plastic_cup_lid", "snack_bag", 
        "straw", "scrap_plastic", "chemical_plastic_bottle", 
        "chemical_plastic_gallon", "chemical_spray_can"
    ],
    "Paper": [
        "reuseable_paper", "scrap_paper", "cardboard_bowl", "cardboard_box"
    ],
    "E-Waste": [
        "battery", "light_bulb"
    ],
    "Others": [
        "stick", "paint_bucket"
    ]
}

st.markdown(
    """
    <style>
    /* Title styling */
    .title {
        font-size: 40px;
        color: #2ecc71;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Subtitle styling */
    .subtitle {
        font-size: 20px;
        color: #BFECFF;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Detection Image */
    .Detection {
        font-size: 20px;
        color: #BFECFF;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Upload section styling */
    .upload-area {
        background-color: #ecf0f1;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Detected objects styling */
    .detected {
        font-size: 18px;
        color: #3498db;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Image grid styling */
    .image-caption {
        text-align: center;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model(model_path):
    return YOLO(model_path)

def detect_objects_and_save(model, image):
    results = model(image)  # Pass the image directly (image can be an array)
    detections = results[0].boxes.data.cpu().numpy()

    annotated_image_array = results[0].plot()
    annotated_image = Image.fromarray(annotated_image_array.astype(np.uint8))

    return detections, results[0].names, annotated_image

def map_to_category(class_name):
    for category, items in CATEGORIES.items():
        if class_name in items:
            return category
    return "Unknown"

def save_to_category_folder(image_path, category, output_dir):
    category_dir = os.path.join(output_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    output_path = os.path.join(category_dir, os.path.basename(image_path))
    shutil.copy(image_path, output_path)

# WebCam Functionality
def display_webcam():

    # Start the webcam
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    model = load_model(MODEL_PATH)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        detections, class_names, annotated_image = detect_objects_and_save(model, frame_rgb)

        # Draw the annotations on the frame (frame_rgb is already in RGB)
        for detection in detections:
            class_id = int(detection[-1])
            class_name = class_names[class_id]
            category = map_to_category(class_name)

            if category != "Unknown":
                x1, y1, x2, y2 = map(int, detection[:4])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{class_name} - {category}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        # Convert the frame back to RGB before showing it in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the annotated frame in Streamlit
        frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

        # Stop the webcam on keypress or break condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Streamlit Upload Section
st.markdown('<div class="title">Waste Categorization</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect and categorize waste items efficiently with our AI-powered tool</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("Process Images"):
    try:
        if not uploaded_files:
            st.error("Please upload at least one image.")
        else:
            model = load_model(MODEL_PATH)
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)

            annotated_images = []

            for uploaded_file in uploaded_files:
                # Save the uploaded file to a temporary location
                temp_image_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Convert the uploaded file to an image
                img = Image.open(temp_image_path)
                img = np.array(img)

                detections, class_names, annotated_image = detect_objects_and_save(model, img)

                detected_objects = []
                for detection in detections:
                    class_id = int(detection[-1])
                    class_name = class_names[class_id]
                    category = map_to_category(class_name)
                    detected_objects.append(f"- Object: {class_name}\n- Category: {category}")

                    if category != "Unknown":
                        save_to_category_folder(temp_image_path, category, OUTPUT_DIR)

                # Save the annotated image
                annotated_image_path = os.path.join(temp_dir, f"annotated_{uploaded_file.name}")
                annotated_image.save(annotated_image_path)

                annotated_images.append((annotated_image_path, uploaded_file.name, detected_objects))

            st.markdown('<div class="Detection">Annotated Images with Detection Info</div>', unsafe_allow_html=True)
            for i in range(0, len(annotated_images), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(annotated_images):
                        img_path, img_name, detections = annotated_images[i + j]
                        with col:
                            st.markdown(f'<div class="detected">Detected objects in {img_name}:</div>', unsafe_allow_html=True)
                            for detection in detections:
                                st.markdown(detection)
                            annotated_image = Image.open(img_path)
                            st.image(annotated_image, caption=img_name)

            shutil.rmtree(temp_dir, ignore_errors=True)

            st.success(f"All uploaded images processed and categorized in **{OUTPUT_DIR}**.")
    except Exception as e:
        st.error(f"Error: {e}")

# Add a button to start webcam processing
if st.button("Start Webcam"):
    display_webcam()
