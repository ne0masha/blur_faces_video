import os
import cv2
import mediapipe as mp

# Укажите путь к вашему видеофайлу
video_path = 'input_files/input_video_5.mp4'
cap = cv2.VideoCapture(video_path)

def process_img(img, face_detection):

    H, W, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W)
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            # print(x1, y1, w, h)

            # blur faces
            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w, :], (30, 30))

    return img

output_dir = 'output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    ret, frame = cap.read()

    output_video = cv2.VideoWriter(os.path.join(output_dir, 'output_video_5.mp4'),
                                   cv2.VideoWriter_fourcc(*'MP4V'),
                                   25,
                                   (frame.shape[1], frame.shape[0]))

    while ret:

        frame = process_img(frame, face_detection)

        output_video.write(frame)

        ret, frame = cap.read()

    cap.release()
    output_video.release()
