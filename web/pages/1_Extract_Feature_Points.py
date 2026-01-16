import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import os.path as osp
import sys
from pages.face.main import Facedetect


# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (load_image_from_upload, 
                   get_facial_landmarks, 
                   draw_facial_landmarks, 
                   process_webcam_image)

# Set page configuration
st.set_page_config(
    page_title="Register Faces",
    page_icon="�",
    layout="wide"
)

# Custom CSS for beautiful design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    h1 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 20px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px 10px 0px 0px;
        color: white;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(255,255,255,0.95);
        color: #0f172a !important; /* dark text on selected tab for contrast */
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stTabs [data-baseweb="tab"][aria-selected="true"] [role="button"] {
        color: #0f172a !important;
    }
    
    .info-box {
        background: rgba(255,255,255,0.1);
        border-left: 4px solid #fbbf24;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(5,150,105,0.2) 100%);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, rgba(239,68,68,0.2) 0%, rgba(220,38,38,0.2) 100%);
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        padding: 12px !important;
        background: rgba(255,255,255,0.9) !important;
        color: #0f172a !important; /* dark input text for readability */
    }
    
    /* Ensure placeholder text is visible on light background */
    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important; /* neutral gray */
        opacity: 1 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16,185,129,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16,185,129,0.6);
    }
    
    p, label {
        color: #f3f4f6 !important;
    }
    </style>
""", unsafe_allow_html=True)

face_detect = Facedetect()

# Page title and description
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>📸 Register Your Face</h1>
        <p style='color: #e0e7ff; font-size: 1.1rem;'>
            Capture and store your facial features for identification
        </p>
    </div>
""", unsafe_allow_html=True)

# Create tabs for image upload and webcam
tab1, tab2 = st.tabs(["📤 Upload Image", "📹 Use Webcam"])

with tab1:
    st.markdown("<h3 style='color: white; text-align: center;'>Upload Photo</h3>", unsafe_allow_html=True)
    
    # Name input at top
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<p style='margin-bottom: 0;'><strong>Your Name:</strong></p>", unsafe_allow_html=True)
        user_name_ = st.text_input("Enter your full name", "", key="text_input_upload", placeholder="Enter your full name")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("📁 Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Validate name is entered
        if not user_name_ or user_name_.strip() == "":
            st.markdown("""
                <div class='error-box'>
                    <strong>❌ Name Required!</strong><br>
                    Please enter your name before registering your face.
                </div>
            """, unsafe_allow_html=True)
        else:
            # Load the image
            image = load_image_from_upload(uploaded_file)
            
            # Create two columns for before/after
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 style='color: white; text-align: center;'>📷 Original Image</h4>", unsafe_allow_html=True)
                st.image(image)
            
            # Process image for landmarks
            with st.spinner("🔍 Detecting facial features..."):
                # Use actual SCRFD detector for face detection
                img_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                st.write("DEBUG: Converting image to BGR format")
                
                bboxes, kpss = face_detect.detector.autodetect(img_cv)
                st.write(f"DEBUG: Detection result - bboxes shape: {bboxes.shape if len(bboxes) > 0 else 'No faces'}, kpss: {len(kpss)}")
                
                if len(bboxes) > 0:
                    # Draw bounding boxes and keypoints on image
                    image_with_landmarks = image.copy()
                    
                    for i, bbox in enumerate(bboxes):
                        # Draw bounding box
                        x1, y1, x2, y2, conf = bbox.astype(int)
                        cv2.rectangle(image_with_landmarks, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image_with_landmarks, f"Face {i+1} ({conf:.2f})", (x1, y1-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Draw keypoints if available
                        if i < len(kpss):
                            kps = kpss[i]
                            for kp in kps:
                                x, y = kp.astype(int)
                                cv2.circle(image_with_landmarks, (x, y), 3, (255, 0, 0), -1)
                    
                    with col2:
                        st.markdown("<h4 style='color: black; text-align: center;'>✨ Features Detected</h4>", unsafe_allow_html=True)
                        st.image(image_with_landmarks)
                    
                    # Display information about detected features
                    st.markdown("<h4 style='color: black;'>📊 Detection Details</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class='success-box'>
                            <strong>✓ Found {len(bboxes)} face(s)</strong><br>
                            Your face has been successfully detected and analyzed!
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Register button
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    with col_btn2:
                        if st.button("✅ Register Face", key="register_upload", use_container_width=True):
                            # Ensure images directory exists
                            face_module_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
                            images_dir = osp.join(face_module_dir, "pages", "face", "data", "images")
                            os.makedirs(images_dir, exist_ok=True)
                            
                            # Save image with person's name
                            image_path = osp.join(images_dir, f"{user_name_.strip()}.jpg")
                            img_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            cv2.imwrite(image_path, img_cv)
                            
                            # Extract features and register
                            feature_point = face_detect.feature(image)
                            
                            if feature_point:
                                face_detect.write_to_csv(user_name_.strip(), image_path, feature_point)
                            st.success(f"✅ **{user_name_} registered successfully!**")
                            st.balloons()
                        else:
                            st.error("❌ Could not extract face features. Please try again.")
                else:
                    st.warning("⚠️ No faces detected in the image. Please try another image.")

with tab2:
    st.header("Enter person name")
    user_name = st.text_input("Enter your name:", "", key="text_input_webcam", placeholder="Required: Enter your full name")

    st.header("Use Webcam")
    
    # Webcam input
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        # Validate name is entered
        if not user_name or user_name.strip() == "":
            st.error("❌ **Name is required!** Please enter your name before registering your face.")
        else:
            # Read image from the buffer
            bytes_data = img_file_buffer.getvalue()
            
            # Convert to an OpenCV image
            file = tempfile.NamedTemporaryFile(delete=False)
            file.write(bytes_data)
            file.close()
            
            img = cv2.imread(file.name)
            os.unlink(file.name)
            
            # Ensure images directory exists
            face_module_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
            images_dir = osp.join(face_module_dir, "pages", "face", "data", "images")
            os.makedirs(images_dir, exist_ok=True)
            
            # Save image with person's name
            image_path = osp.join(images_dir, f"{user_name.strip()}.jpg")
            cv2.imwrite(image_path, img)
            
            # Extract features and register
            feature_point = face_detect.feature(img)
            
            if feature_point:
                face_detect.write_to_csv(user_name.strip(), image_path, feature_point)
                st.success(f"✅ **{user_name} registered successfully!**")
                st.balloons()
            else:
                st.error("❌ No faces detected in the image. Please try again.")

# Display registered faces section
st.markdown("---")
st.header("📸 Registered Faces Gallery")
st.write("View all previously registered faces in the database.")
# Load registered faces
# Use absolute path relative to the pages/face directory
face_module_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
registered_faces_dir = osp.join(face_module_dir, "pages", "face", "data", "images")
csv_file = osp.join(face_module_dir, "pages", "face", "data", "data.csv")

if os.path.exists(registered_faces_dir):
    image_files = sorted([f for f in os.listdir(registered_faces_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    if image_files:
        # Create columns to display faces
        cols = st.columns(3)
        
        for idx, image_file in enumerate(image_files):
            col = cols[idx % 3]
            
            with col:
                try:
                    img_path = os.path.join(registered_faces_dir, image_file)
                    img = Image.open(img_path)
                    
                    # Extract person name from filename
                    person_name = image_file.replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
                    
                    # Create a container for the image and delete button
                    container = st.container(border=True)
                    
                    with container:
                        # Display image
                        st.image(img, caption=person_name)
                        
                        # Create delete button
                        if st.button(f"🗑️ Delete {person_name}", key=f"delete_{person_name}_{idx}"):
                            try:
                                # Delete image file
                                os.remove(img_path)
                                
                                # Delete from CSV
                                if os.path.exists(csv_file):
                                    import pandas as pd
                                    try:
                                        df = pd.read_csv(csv_file)
                                        df = df[df['name'] != person_name]
                                        df.to_csv(csv_file, index=False)
                                    except:
                                        # Manual CSV update if pandas fails
                                        with open(csv_file, 'r') as f:
                                            lines = f.readlines()
                                        
                                        with open(csv_file, 'w') as f:
                                            for line in lines:
                                                if not line.startswith(person_name + ','):
                                                    f.write(line)
                                
                                st.success(f"✅ {person_name} deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error deleting {person_name}: {e}")
                
                except Exception as e:
                    st.warning(f"Could not load {image_file}")
    else:
        st.info("No registered faces yet. Register your face to get started!")
else:
    st.info("Registered faces directory not found.")

# Footer with return to main page
st.markdown("---")
st.page_link("app.py", label="Return to Main Page", icon="🏠")
