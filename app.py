import streamlit as st
import torch
from pytube import YouTube
import cv2
import tempfile
import os
from ultralytics import RTDETR
import numpy as np


# Загрузка модели Ultralytics
model = RTDETR('best.pt')  # убедитесь, что файл best.pt находится в правильной директории


def draw_boxes(frame, results):
    # Проверка, не пусты ли результаты
    if len(results) == 0:
        return frame  # Возвращение неизмененного кадра, если результаты пусты

    for det in results:
        # Возможно, потребуется адаптировать эту логику в соответствии с форматом данных
        if len(det) >= 5 and det[4] > conf_thres:  # Проверка наличия нужных данных
            x1, y1, x2, y2, conf, cls =det[:6]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0),
                          2)  # Рисование ограничивающей рамки
            cv2.putText(frame, f'{cls} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0),
                        2)  # Добав

    return frame

# Функция для обработки видео
def process_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Обработка кадра с помощью модели
        results = model(frame)

        # Рендеринг ограничивающих рамок и классов на кадре
        frame = draw_boxes(frame, results)

        # Отображение обработанного кадра
        stframe.image(frame, channels="BGR", use_column_width=True)

    cap.release()

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
