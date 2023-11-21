import streamlit as st
import torch
from pytube import YouTube
import cv2
import tempfile
import os
from ultralytics import YOLO

# Загрузка модели Ultralytics
model = YOLO('best_yolo.pt')  # убедитесь, что файл best_yolo.pt находится в правильной директории

def draw_boxes(frame, detections):
    for det in detections:
        if len(det) >= 6:
            x1, y1, x2, y2, conf, cls = det
            if conf > 0.25:  # Установите порог уверенности

                # Корректировка координат рамки
                x1, y1, x2, y2 = max(0, int(x1)), max(0, int(y1)), min(int(x2), frame.shape[1]), min(int(y2), frame.shape[0])

                # Получение названия класса
                label = f'{model.names[int(cls)]} {conf:.2f}'

                # Установка толщины рамки и размера шрифта
                box_thickness = 3
                font_scale = 0.7
                font_thickness = 2

                # Рисование ограничивающей рамки
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), box_thickness)

                # Рисование подписи
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    return frame



def process_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Обработка кадра с помощью модели
        results = model(frame)
        detections = results if isinstance(results, list) else results.xyxy[0]

        # Рендеринг ограничивающих рамок и классов на кадре
        frame = draw_boxes(frame, detections)

        # Отображение обработанного кадра
        stframe.image(frame, channels="BGR", use_column_width=True)

    cap.release()

# ... (остальная часть кода)



# Функция для скачивания видео с YouTube
def download_youtube_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').first()
    temp_dir = tempfile.mkdtemp()
    video_path = stream.download(output_path=temp_dir)
    return video_path

# ... (остальная часть кода)


# ... (остальная часть кода)

# Создание интерфейса Streamlit
st.title("Детекция дорожных знаков на видео")

# Ввод ссылки на YouTube
youtube_url = st.text_input("Вставьте ссылку на YouTube видео")

if youtube_url:
    with st.spinner('Скачиваем видео...'):
        video_path = download_youtube_video(youtube_url)
        st.success('Видео скачано!')
        process_video(video_path, model)
        os.remove(video_path)  # Удаление скачанного файла после обработки

# Загрузка видео напрямую
else:
    uploaded_file = st.file_uploader("Или загрузите видео файл", type=["mp4", "avi"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        process_video(tfile.name, model)
        tfile.close()
