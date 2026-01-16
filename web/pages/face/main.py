#!/usr/bin/env python

import os
import cv2
import csv
import base64
import numpy as np
import onnxruntime
import os.path as osp
from pages.face.scrfd import SCRFD
from pages.face.arcface_onnx import ArcFaceONNX

onnxruntime.set_default_logger_severity(3)

class Facedetect():
    def __init__(self):
        # Get the directory of this file to build absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create data folder structure
        self.data_dir = os.path.join(current_dir, "data")
        self.images_dir = os.path.join(self.data_dir, "images")
        self.csv_file = os.path.join(self.data_dir, "data.csv")
        
        # Ensure directories exist
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Ensure CSV file exists with headers
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["name", "image_path", "feature"])
        
        # Use absolute paths for models
        det_model = os.path.join(current_dir, 'det_10g.onnx')
        rec_model = os.path.join(current_dir, 'w600k_r50.onnx')
        
        self.detector = SCRFD(det_model)
        print(f"DEBUG: SCRFD detector loaded from {det_model}")
        self.detector.prepare(0)
        print(f"DEBUG: SCRFD detector prepared - det_thresh={self.detector.det_thresh}, nms_thresh={self.detector.nms_thresh}")
        
        # Try to load ArcFace model, use CPU provider if CUDA not available
        try:
            self.rec = ArcFaceONNX(rec_model)
            self.rec.prepare(0)
        except FileNotFoundError:
            print("Warning: ArcFace model 'w600k_r50.onnx' not found. Some features will be limited.")
            self.rec = None
        except Exception as e:
            print(f"Warning: Could not load ArcFace model: {e}. Using CPU provider.")
            try:
                # Retry with explicit CPU provider
                import onnxruntime as rt
                ort_session = rt.InferenceSession(rec_model, providers=['CPUExecutionProvider'])
                self.rec = ArcFaceONNX(session=ort_session)
                self.rec.prepare(0)
            except:
                self.rec = None
        
        self.data_dict = {}

    def write_to_csv(self, name, image_path, feature):
        # Use absolute path based on this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", "data.csv")
        directory = os.path.dirname(file_path)
        
        # Create the directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_exists = os.path.isfile(file_path)
        
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if file does not exist
            if not file_exists:
                writer.writerow(["name", "image_path", "feature"])
            
            # Write data
            writer.writerow([name, image_path, feature])

    def load_csv_to_dict(self):
        # Use absolute path based on this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", "data.csv")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # If file doesn't exist, return empty dict (graceful handling for first startup)
        if not os.path.exists(file_path):
            return {}

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Read the header row
            
            if headers != ["name", "image_path", "feature"]:
                print("CSV format mismatch! Expected columns: name, image_path, feature.")
                return {}

            for row in reader:
                if len(row) != 3:
                    continue  # Skip invalid rows
                
                name, image_path, feature = row
                self.data_dict[feature] = {"name": name, "image_path": image_path}


    def feature(self, image):
        if self.rec is None:
            print("ERROR: ArcFace model not loaded")
            return None
        
        print(f"DEBUG: Detecting faces in image with shape: {image.shape if hasattr(image, 'shape') else 'unknown'}")
        bboxes, kpss = self.detector.autodetect(image, max_num=1)
        print(f"DEBUG: Detection returned {len(bboxes)} faces")
        
        if len(kpss) == 0:
            print("WARNING: No faces detected during feature extraction")
            return None
        
        print(f"DEBUG: Extracting feature for first face")    
        kps = kpss[0]
        feature_point = self.rec.get(image, kps)
        feature_string = " ".join(map(str, feature_point))
        feature_bytes = feature_string.encode("utf-8")
        encoded_data = base64.b64encode(feature_bytes)
        feature_str = encoded_data.decode("utf-8")
        
        print(f"DEBUG: Feature extraction successful, encoded length: {len(feature_str)}")
        return feature_str

    def base64_to_array(self, encode_feature):
        try:
            if not encode_feature or encode_feature.strip() == '':
                return np.array([])
            
            decoded_data = base64.b64decode(encode_feature)
            decoded_string = decoded_data.decode("utf-8")
            data_list = list(map(float, decoded_string.split()))
            
            if len(data_list) == 0:
                return np.array([])
            
            return np.array(data_list)
        except Exception as e:
            print(f"Error decoding feature: {e}")
            return np.array([])

    def detect(self, image):
        if image is None:
            print("Image not found or unable to read")
            return []
        
        if self.rec is None:
            print("ArcFace model not available for detection")
            return []
        
        bboxes, kpss = self.detector.autodetect(image)
        matches = []

        if len(bboxes) != 0:
            for index in range(len(bboxes)):
                try:
                    detect_feature = self.rec.get(image, kpss[index])
                    best_match = None
                    best_similarity = 0.28  # Threshold
                    
                    for feature, details in self.data_dict.items():
                        try:
                            feature_data = self.base64_to_array(feature)
                            
                            # Skip if feature data is empty or invalid shape
                            if len(feature_data) == 0 or len(detect_feature) == 0:
                                continue
                            
                            # Ensure both features have the same shape
                            if len(detect_feature) != len(feature_data):
                                continue
                            
                            sim = self.rec.compute_sim(detect_feature, feature_data)
                            
                            # Keep track of best match
                            if sim > best_similarity:
                                best_similarity = sim
                                best_match = {
                                    'name': details['name'],
                                    'image_path': details['image_path'],
                                    'similarity': sim
                                }
                                print(f"Match Found! Name: {details['name']}, Similarity: {sim:.4f}")
                        except Exception as e:
                            continue
                    
                    # Add match to results
                    if best_match:
                        bbox = bboxes[index]
                        best_match['bbox'] = bbox
                        matches.append(best_match)
                    else:
                        # Unknown face
                        bbox = bboxes[index]
                        matches.append({
                            'name': 'Unknown',
                            'image_path': '',
                            'similarity': 0,
                            'bbox': bbox
                        })
                except Exception as e:
                    print(f"Error processing face {index}: {e}")
                    continue
        
        return matches

