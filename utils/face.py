import numpy as np
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('arial.ttf', size=14)

def visualize(image, face, text, box_color=(0, 255, 0), text_color=(0, 0, 255)):
    output = Image.fromarray(image)  # Convert OpenCV image to PIL format
    draw = ImageDraw.Draw(output)
    if face is not None:
        bbox = face[0:4].astype(np.int32)
        draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])], outline=box_color, width=2)
        draw.text((bbox[0], bbox[1] - 15), text, fill=text_color, font=font)
    return np.array(output)


def detect_face(detector, sface, image):
    detections = detector.detect(image)
    faces = np.array([]) if detections[1] is None else detections[1]
    if(faces.size != 0):
        detected_face = faces[0][:-1]
        score = faces[0][-1]
        aligned_face = sface.alignCrop(image, detected_face)
        detected_face_features = sface.feature(aligned_face)
        return (detected_face, detected_face_features, score)
    return None
     
def match_face(sface, features1, features2):
    isMatched = False
    score1 = sface.match(features1, features2, 0)
    score2 = sface.match(features1, features2, 1)
    #print(score1, score2)
    if score1 >0.5:
        isMatched = True
    return isMatched
    