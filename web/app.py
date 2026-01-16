import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Facial Recognition App",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container */
    .main {
        background: transparent;
    }
    
    /* Title styling */
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2 {
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    h3 {
        color: #e0e7ff !important;
        font-size: 1.3rem;
    }
    
    /* Text styling */
    p {
        color: #f3f4f6 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Cards styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }

    /* Light card variants (use darker text for contrast) */
    .card.light, .card-light {
        color: #0f172a;
    }

    .card.light p,
    .card.light ul,
    .card.light ul li,
    .card-light p,
    .card-light ul,
    .card-light ul li {
        color: #374151 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stFileUploader > div > div,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e0e7ff !important;
        padding: 10px !important;
        font-size: 1rem !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
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
        color: #0f172a !important; /* force dark text for better contrast on light tab background */
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stTabs [data-baseweb="tab"][aria-selected="true"] [role="button"] {
        color: #0f172a !important;
    }
    
    /* Column text */
    .element-container {
        margin: 1rem 0;
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Links */
    a {
        color: #fbbf24 !important;
        text-decoration: none;
        font-weight: 600;
    }
    
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Main page content
st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1>👤 Facial Recognition App</h1>
        <p style='font-size: 1.3rem; color: #e0e7ff;'>Advanced Face Detection & Recognition System</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center; color: #f3f4f6; margin-bottom: 2rem;'>
    🚀 Experience cutting-edge facial recognition technology with real-time processing and high accuracy
    </p>
""", unsafe_allow_html=True)

# Create two columns for feature cards
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
            <div class='card light' style='background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,249,255,0.95) 100%); 
                    border-radius: 15px; padding: 2.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border-left: 5px solid #667eea;'>
            <h3 style='color: #667eea; margin-top: 0; display: flex; align-items: center;'>
                <span style='font-size: 2rem; margin-right: 10px;'>📸</span> Register Faces
            </h3>
            <p style='color: #4b5563; line-height: 1.8;'>
                <strong>Capture and store faces</strong> using your webcam or upload images. 
                Our system automatically extracts facial features and creates a secure database 
                for future identification.
            </p>
            <ul style='color: #4b5563;'>
                <li>✨ Real-time webcam capture</li>
                <li>📷 Upload images directly</li>
                <li>🎯 Automatic face detection</li>
                <li>💾 Secure storage</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Go to Register Faces", key="btn_register", use_container_width=True):
        st.switch_page("pages/1_Extract_Feature_Points.py")

with col2:
    st.markdown("""
        <div class='card light' style='background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,253,250,0.95) 100%); 
                border-radius: 15px; padding: 2.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                border-left: 5px solid #10b981;'>
            <h3 style='color: #10b981; margin-top: 0; display: flex; align-items: center;'>
                <span style='font-size: 2rem; margin-right: 10px;'>🔍</span> Identify Faces
            </h3>
            <p style='color: #4b5563; line-height: 1.8;'>
                <strong>Recognize and identify faces</strong> from your database with high accuracy. 
                Compare new images against registered faces and get instant results with 
                similarity scores.
            </p>
            <ul style='color: #4b5563;'>
                <li>⚡ Real-time identification</li>
                <li>📊 Similarity scoring</li>
                <li>🎥 Webcam support</li>
                <li>✔️ Instant results</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Go to Identify Faces", key="btn_identify", use_container_width=True):
        st.switch_page("pages/2_Identify_Faces.py")

# Add divider
st.markdown("<hr style='border: 2px solid rgba(255,255,255,0.2); margin: 3rem 0;'>", unsafe_allow_html=True)

# How it works section
st.markdown("""
    <h2 style='text-align: center; margin-top: 3rem;'>⚙️ How It Works</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h3 style='font-size: 2.5rem; margin: 0;'>1️⃣</h3>
            <h4 style='color: #fbbf24;'>Detect Faces</h4>
            <p style='color: #e0e7ff;'>
                SCRFD model identifies faces in real-time using advanced neural networks
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h3 style='font-size: 2.5rem; margin: 0;'>2️⃣</h3>
            <h4 style='color: #fbbf24;'>Extract Features</h4>
            <p style='color: #e0e7ff;'>
                ArcFace technology extracts unique 512-dimensional face embeddings
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h3 style='font-size: 2.5rem; margin: 0;'>3️⃣</h3>
            <h4 style='color: #fbbf24;'>Identify Match</h4>
            <p style='color: #e0e7ff;'>
                Compare and find matches with accuracy above 99%
            </p>
        </div>
    """, unsafe_allow_html=True)

# Technology stack
st.markdown("<hr style='border: 2px solid rgba(255,255,255,0.2); margin: 3rem 0;'>", unsafe_allow_html=True)

st.markdown("""
    <h2 style='text-align: center;'>🛠️ Technology Stack</h2>
""", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4, gap="medium")

with tech_col1:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 1.5rem; border-radius: 10px;'>
            <p style='font-size: 2rem;'>🎨</p>
            <p style='color: #fbbf24; font-weight: 600;'>Streamlit</p>
            <p style='color: #e0e7ff; font-size: 0.9rem;'>Web Framework</p>
        </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 1.5rem; border-radius: 10px;'>
            <p style='font-size: 2rem;'>🤖</p>
            <p style='color: #fbbf24; font-weight: 600;'>ONNX Runtime</p>
            <p style='color: #e0e7ff; font-size: 0.9rem;'>Model Inference</p>
        </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 1.5rem; border-radius: 10px;'>
            <p style='font-size: 2rem;'>🖼️</p>
            <p style='color: #fbbf24; font-weight: 600;'>OpenCV</p>
            <p style='color: #e0e7ff; font-size: 0.9rem;'>Image Processing</p>
        </div>
    """, unsafe_allow_html=True)

with tech_col4:
    st.markdown("""
        <div style='text-align: center; background: rgba(255,255,255,0.1); 
                    padding: 1.5rem; border-radius: 10px;'>
            <p style='font-size: 2rem;'>📊</p>
            <p style='color: #fbbf24; font-weight: 600;'>Python</p>
            <p style='color: #e0e7ff; font-size: 0.9rem;'>Core Language</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border: 2px solid rgba(255,255,255,0.2); margin: 3rem 0;'>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem;'>
        <p style='color: #e0e7ff; font-size: 0.95rem;'>
            ✨ Built with ❤️ using Streamlit, OpenCV, and ONNX Runtime
        </p>
        <p style='color: #cbd5e1; font-size: 0.85rem; margin-top: 1rem;'>
            © 2024 Facial Recognition App | Advanced AI-Powered Face Recognition System
        </p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Facial Recognition App | Built with Streamlit, OpenCV and face_recognition")
