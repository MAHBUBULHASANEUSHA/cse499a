---

# EcoVision

EcoVision is an AI-powered image detection and categorization tool that helps identify and classify waste items into specific categories such as Plastic, Paper, E-Waste, and Others. This tool uses the YOLOv8 model for object detection and displays visually appealing results.

---

## Features
1. Detects waste items in images.
2. Categorizes waste items into:
   - Plastic
   - Paper
   - E-Waste
   - Others
3. Saves categorized images into respective folders.
4. Provides a clean and visually appealing interface.
5. Displays annotated images with detected objects.

---

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd EcoVision
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
1. **Run the application**:
   ```bash
   streamlit run app.py
   ```
2. **Upload images**:
   - Use the "Upload images" section to upload multiple images.
3. **Process images**:
   - Click the "Process Images" button to detect and categorize objects.
4. **View results**:
   - Detected objects and their categories will be displayed along with annotated images.
5. **Categorized outputs**:
   - Categorized images are saved in the `categorized_images` directory.

---

## Project Structure
- **app.py**: The main Streamlit application file.
- **best.pt**: Pretrained YOLOv8 model file (ensure it is in the project directory).
- **categorized_images/**: Directory where categorized images are saved.
- **requirements.txt**: File containing the required Python dependencies.

---

## Requirements
- Python 3.8 or higher
- Streamlit
- Ultralytics (YOLOv8)
- PIL (Pillow)
- NumPy
- shutil

---

## Categories
EcoVision categorizes detected objects into the following categories:
1. **Plastic**:
   - plastic_bag, plastic_bottle, plastic_box, etc.
2. **Paper**:
   - reuseable_paper, cardboard_box, etc.
3. **E-Waste**:
   - battery, light_bulb, etc.
4. **Others**:
   - stick, paint_bucket, etc.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
- [YOLOv8 by Ultralytics](https://ultralytics.com/yolov8) for the object detection model.
- Streamlit for the web interface.

---

Let me know if you need any further modifications!