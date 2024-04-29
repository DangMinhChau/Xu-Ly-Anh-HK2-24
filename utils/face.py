import cv2 as cv
import numpy as np

def visualize(image, face, text, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    output = image.copy()
    if fps is not None:
        cv.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color)
    if face is not None:
        bbox = face[0:4].astype(np.int32)
        cv.rectangle(output, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), box_color, 2)
        cv.putText(output, '{}'.format(text), (bbox[0], bbox[1]-15), cv.FONT_HERSHEY_DUPLEX, 0.5, text_color)
    return output


def detect_face(detector, sface, image):
    detections = detector.detect(image)
    faces = np.array([]) if detections[1] is None else detections[1]
    detected_face = None
    score = 0
    if(faces.size != 0):
        detected_face = faces[0][:-1]
        score = faces[0][-1]
        aligned_face = sface.alignCrop(image, detected_face)
        detected_face_features = sface.feature(aligned_face)
        return (detected_face, detected_face_features, score)
    return None
     
def match_face(sface, features1, features2):
    isMatched = False
    score = sface.match(features1, features2, 0)
    if score >= 0.6:
        isMatched = True
    return isMatched
    