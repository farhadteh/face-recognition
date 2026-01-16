import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import sys
import time
from pages.face.main import Facedetect

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (load_image_from_upload, get_face_locations, draw_face_boxes, 
                   process_webcam_image)

# Set page configuration
st.set_page_config(
    page_title="Identify Faces",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for beautiful design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    h1, h2, h3, h4, h5 {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    h1 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .match-found {
        background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(5,150,105,0.2) 100%);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #e0e7ff;
    }
    
    .no-match {
        background: linear-gradient(135deg, rgba(239,68,68,0.2) 0%, rgba(220,38,38,0.2) 100%);
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #e0e7ff;
    }
    
    .similarity-bar {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
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
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(59,130,246,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59,130,246,0.6);
    }
    
    p, label {
        color: #f3f4f6 !important;
    }
    
    .expander {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

face_detect = Facedetect()
face_detect.load_csv_to_dict()

# Page title and description
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>🔍 Identify Faces</h1>
        <p style='color: #e0e7ff; font-size: 1.1rem;'>
            Compare and identify faces with high accuracy
        </p>
    </div>
""", unsafe_allow_html=True)

# Create tabs for image upload and webcam
identify_tab1, identify_tab2 = st.tabs(["📤 Upload Image", "📹 Use Webcam"])

with identify_tab1:
    st.markdown("<h3 style='color: white; text-align: center;'>Upload Photo for Identification</h3>", unsafe_allow_html=True)
    
    # File uploader for identification
    identify_file = st.file_uploader("📁 Upload image for face detection", type=["jpg", "jpeg", "png"], key="identify_upload")
    
    if identify_file is not None:
        # Load the image
        identify_image = load_image_from_upload(identify_file)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='color: white; text-align: center;'>📷 Original Image</h4>", unsafe_allow_html=True)
            st.image(identify_image)
        
        # Process image for face detection and identification
        with st.spinner("🔍 Detecting and identifying faces..."):
            # Convert PIL image to OpenCV format
            img_cv = cv2.cvtColor(identify_image, cv2.COLOR_RGB2BGR)
            matches = face_detect.detect(img_cv)
            
            if matches:
                with col2:
                    st.markdown("<h4 style='color: white; text-align: center;'>✨ Results</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class='match-found'>
                            <strong>✓ Found {len(matches)} face(s)</strong>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Display all matches in expandable sections
                for i, match in enumerate(matches):
                    with st.expander(f"👤 Face #{i+1} Details", expanded=True):
                        match_col1, match_col2 = st.columns(2)
                        
                        with match_col1:
                            st.markdown("<h5 style='color: white;'>Detected Face</h5>", unsafe_allow_html=True)
                            # Extract and display detected face
                            bbox = match['bbox']
                            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                            face_crop = identify_image[y1:y2, x1:x2]
                            st.image(face_crop)
                        
                        with match_col2:
                            if match['name'] != 'Unknown':
                                st.markdown("<h5 style='color: white;'>Registered Face</h5>", unsafe_allow_html=True)
                                # Display registered image
                                try:
                                    registered_img = cv2.imread(match['image_path'])
                                    if registered_img is not None:
                                        registered_rgb = cv2.cvtColor(registered_img, cv2.COLOR_BGR2RGB)
                                        st.image(registered_rgb)
                                except:
                                    st.info("Could not load registered image")
                            else:
                                st.markdown("<h5 style='color: white;'>Status</h5>", unsafe_allow_html=True)
                                st.info("🤔 No match found in database")
                        
                        # Display match results
                        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
                        
                        if match['name'] != 'Unknown':
                            similarity = match.get('similarity', 0)
                            st.markdown(f"""
                                <div class='match-found'>
                                    <strong>✅ Match Found: {match['name']}</strong><br>
                                    Similarity Score: <strong>{similarity:.2%}</strong>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                                <div class='no-match'>
                                    <strong>❌ No Match Found</strong><br>
                                    This face is not in the database
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='no-match'>
                        <strong>⚠️ No Faces Detected</strong><br>
                        Please try another image with clear faces
                    </div>
                """, unsafe_allow_html=True)

with identify_tab2:
    st.markdown("<h3 style='color: white; text-align: center;'>Identify Using Webcam</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e0e7ff;'>📹 Take a photo with your webcam for real-time identification</p>", unsafe_allow_html=True)
    
    # Webcam input
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        # Read image from the buffer and convert to numpy array
        bytes_data = img_file_buffer.getvalue()
        np_arr = np.frombuffer(bytes_data, np.uint8)
        
        # Convert to an OpenCV image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='color: white; text-align: center;'>📷 Captured Image</h4>", unsafe_allow_html=True)
            st.image(img_rgb)

        # Process image for face detection and identification
        with st.spinner("🔍 Processing webcam image..."):
            matches = face_detect.detect(img)
            
            if matches:
                with col2:
                    st.markdown("<h4 style='color: white; text-align: center;'>✨ Results</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class='match-found'>
                            <strong>✓ Found {len(matches)} face(s)</strong>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Display all matches in expandable sections
                for i, match in enumerate(matches):
                    with st.expander(f"👤 Face #{i+1} Details", expanded=True):
                        match_col1, match_col2 = st.columns(2)
                        
                        with match_col1:
                            st.markdown("<h5 style='color: white;'>Detected Face</h5>", unsafe_allow_html=True)
                            # Extract and display detected face
                            bbox = match['bbox']
                            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                            face_crop = img_rgb[y1:y2, x1:x2]
                            st.image(face_crop)
                        
                        with match_col2:
                            if match['name'] != 'Unknown':
                                st.markdown("<h5 style='color: white;'>Registered Face</h5>", unsafe_allow_html=True)
                                # Display registered image
                                try:
                                    registered_img = cv2.imread(match['image_path'])
                                    if registered_img is not None:
                                        registered_rgb = cv2.cvtColor(registered_img, cv2.COLOR_BGR2RGB)
                                        st.image(registered_rgb)
                                except:
                                    st.info("Could not load registered image")
                            else:
                                st.markdown("<h5 style='color: white;'>Status</h5>", unsafe_allow_html=True)
                                st.info("🤔 No match found in database")
                        
                        # Display match results
                        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
                        
                        if match['name'] != 'Unknown':
                            similarity = match.get('similarity', 0)
                            st.markdown(f"""
                                <div class='match-found'>
                                    <strong>✅ Match Found: {match['name']}</strong><br>
                                    Similarity Score: <strong>{similarity:.2%}</strong>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                                <div class='no-match'>
                                    <strong>❌ No Match Found</strong><br>
                                    This face is not in the database
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='no-match'>
                        <strong>⚠️ No Faces Detected</strong><br>
                        Please ensure your face is clearly visible and try again
                    </div>
                """, unsafe_allow_html=True)
