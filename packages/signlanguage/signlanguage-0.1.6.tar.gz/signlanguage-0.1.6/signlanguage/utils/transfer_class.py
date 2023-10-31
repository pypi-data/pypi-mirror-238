import cv2
import json
import mediapipe as mp
import time


class dataDetection:
    def recog_model_handler_body(self, results=None, model_object=None, mp_holistic=None):
        #image_height, image_width, _ = image.shape
        image_height = 256
        image_width = 256
        model_object['model_body'].append({
                "index": "NOSE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE_INNER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE_OUTER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE_INNER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE_OUTER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EAR",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EAR",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].y * image_height
            })
        model_object['model_body'].append({
                "index": "MOUTH_LEFT",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].y * image_height
            })
        model_object['model_body'].append({
                "index": "MOUTH_RIGHT",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_SHOULDER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_SHOULDER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_ELBOW",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_ELBOW",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_WRIST",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_WRIST",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_PINKY",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_PINKY",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_INDEX",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_INDEX",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_THUMB",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_THUMB",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].y * image_height
            })

    def recog_model_handler_hand(self, connection_landmark=None, model_object=None, direction=None, mp_holistic=None):
        #image_height, image_width, _ = image.shape
        image_height = 256
        image_width = 256
        model_object['model_hand_'+direction].append({
                "index": "WRIST",
                "x": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].x,
                "y": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].y,
                "z": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].x * image_width,
                "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].z * image_width,
                "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].y * image_height
            })
        model_object['model_hand_'+direction].append({
        "index": "THUMB_CMC",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_IP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].y * image_height
        })


class dataCreation:

    def recog_model_handler_body(self, results=None, model_object=None, mp_holistic=None):
        #image_height, image_width, _ = image.shape
        image_height = 256
        image_width = 256
        model_object['model_body'].append({
                "index": "NOSE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE_INNER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_INNER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EYE_OUTER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE_INNER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EYE_OUTER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_EAR",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_EAR",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].y * image_height
            })
        model_object['model_body'].append({
                "index": "MOUTH_LEFT",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].y * image_height
            })
        model_object['model_body'].append({
                "index": "MOUTH_RIGHT",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_SHOULDER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_SHOULDER",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_ELBOW",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_ELBOW",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_WRIST",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_WRIST",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_PINKY",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_PINKY].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_PINKY",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_PINKY].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_INDEX",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_INDEX",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y * image_height
            })
        model_object['model_body'].append({
                "index": "LEFT_THUMB",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_THUMB].y * image_height
            })
        model_object['model_body'].append({
                "index": "RIGHT_THUMB",
                "x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].x,
                "y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].y,
                "z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].z,
                "width": image_width,
                "height": image_height,
                "transform_x": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].x * image_width,
                "transform_z": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].z * image_width,
                "transform_y": results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_THUMB].y * image_height
            })

    def recog_model_handler_hand(self, connection_landmark=None, model_object=None, direction=None, mp_holistic=None):
        #image_height, image_width, _ = image.shape
        image_height = 256
        image_width = 256
        model_object['model_hand_'+direction].append({
                "index": "WRIST",
                "x": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].x,
                "y": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].y,
                "z": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].z,
                "width": image_width,
                "height": image_height,
                "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].x * image_width,
                "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].z * image_width,
                "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.WRIST].y * image_height
            })
        model_object['model_hand_'+direction].append({
        "index": "THUMB_CMC",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_CMC].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_IP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_IP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "THUMB_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.THUMB_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "INDEX_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "MIDDLE_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "RING_FINGER_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_MCP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_MCP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_PIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_PIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_DIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_DIP].y * image_height
        })

        model_object['model_hand_'+direction].append({
        "index": "PINKY_TIP",
        "x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].x,
        "y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].y,
        "z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].z,
        "width": image_width,
        "height": image_height,
        "transform_x": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].x * image_width,
        "transform_z": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].z * image_width,
        "transform_y": connection_landmark.landmark[mp_holistic.HandLandmark.PINKY_TIP].y * image_height
        })

    def create_data(self, real_capture=None, video_path=None, url_pathFolder=None, label=None, qty_Data=None):

        print(f"------------------------------------------------------------------------------------")

        if None in (url_pathFolder, label, qty_Data):
            print(f"[Creation Data] - no puede crearse la data solicitada, se requiere [url_pathFolder, label]")
            return None

        if real_capture is None and video_path is None:
            print(f"[Creation Data] - no puede crearse la data solicitada, se requiere [real_capture] o [video_path]")
            return None
        
        if not real_capture and video_path is None:
            print(f"[Creation Data] - no puede crearse la data solicitada, se requiere [video_path]")
            return None


        mp_holistic = mp.solutions.holistic
        file = 0
        cap = cv2.VideoCapture(0) if real_capture else cv2.VideoCapture(video_path)
        time.sleep(5)
        print(f" Starting creation model data-------------------------------------")
        
        with mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            refine_face_landmarks=True) as holistic:
            
            while cap.isOpened():
                model_object = {
                "model_body": [],
                "model_hand_Right": [],
                "model_hand_Left": []
                }
                success, image = cap.read()
                if not success:
                    print(" Ignoring empty camera frame-------------------------------------")
                    continue

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results  = holistic.process(image)

                if results.pose_landmarks:
                    self.recog_model_handler_body(results=results, model_object=model_object, mp_holistic=mp_holistic)

                    if results.left_hand_landmarks:
                        self.recog_model_handler_hand(connection_landmark=results.left_hand_landmarks, direction="Left", model_object=model_object, mp_holistic=mp_holistic)
                    
                    if results.right_hand_landmarks:
                        self.recog_model_handler_hand(connection_landmark=results.right_hand_landmarks, direction="Right", model_object=model_object, mp_holistic=mp_holistic)


                    if (results.left_hand_landmarks or results.right_hand_landmarks): 
                        try:
                            json_object = json.dumps(model_object, indent=4)
                            with open(f"{url_pathFolder}\\{label}{file}.json", "w") as outfile:
                                outfile.write(json_object)
                            
                            print(f"FILE: {url_pathFolder}\\{label}{file}.json --- was created")
                            file = file +1  
                        except Exception as e:
                            print(f"FILE: {url_pathFolder}\\{label}{file}.json --- was not created, Error: {e}")

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.flip(image, 1)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow('MediaPipe Hands', image )
                
                if cv2.waitKey(5) & 0xFF == 27 or file == qty_Data:
                    print(f" Ended creation model data-------------------------------------")
                    print(f"------------------------------------------------------------------------------------")
                    break

        cap.release()


