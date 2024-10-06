import os
import cv2
import mediapipe as mp
import numpy as np


def process_img(img, face_detection):
    H, W, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x_min, y_min, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x_min = int(x_min * W)
            y_min = int(y_min * H)
            w = int(w * W)
            h = int(h * H)

            # Увеличиваем высоту размываемого фрагмента на 1/3 для лба
            additional_height = int(h / 3)
            y_min = max(0, y_min - additional_height)  # y_min не выходит за пределы изображения
            h += additional_height  # Увеличиваем высоту

            # Рассчитываем центр и размеры овала
            center_x = x_min + w // 2
            center_y = y_min + h // 2
            axes = (w // 2, h // 2)  # Полуоси овала

            # Создаем маску овала
            mask = np.zeros_like(img, dtype=np.uint8)
            cv2.ellipse(mask, (center_x, center_y), axes, 0, 0, 360, (255, 255, 255), -1)  # Белый овал на черном фоне

            # Размываем область, соответствующую овалу
            blurred_face = cv2.blur(img, (70, 70))
            img = np.where(mask == 255, blurred_face, img)  # Заменяем область овала на размытое изображение

            # Для отладки: отображаем маску
            #cv2.imshow("Mask", mask)
            #cv2.waitKey(1)

    return img


output_dir = 'output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.1) as face_detection:
    for i in ('1', '2', '3'):
        video_path = 'input_files/input_video_'+i+'.mp4'
        cap = cv2.VideoCapture(video_path)

        ret, frame = cap.read()

        output_video = cv2.VideoWriter(os.path.join(output_dir, 'output_video_'+i+'.mp4'),
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (frame.shape[1], frame.shape[0]))

        while ret:

            frame = process_img(frame, face_detection)

            output_video.write(frame)

            ret, frame = cap.read()


        cap.release()
        output_video.release()