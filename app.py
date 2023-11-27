"""
Основной модуль Streamlit для детекции дорожных знаков на видео.
"""

import random
import tempfile
import os
import requests
import streamlit as st
import numpy as np
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
import cv2  # pylint: disable=no-member
from ultralytics import YOLO
from ultralytics.engine.results import Results
from config import MODEL_URL, MODEL_DESTINATION


def download_file(url: str, destination: str) -> None:
    """
    Скачивает файл по указанному URL и сохраняет его в назначенном месте.
    Параметры:
    - url: URL-адрес для скачивания файла.
    - destination: Путь сохранения файла.
    """
    if not os.path.exists(destination):
        response = requests.get(url, timeout=10)
        with open(destination, "wb") as file:
            file.write(response.content)


def draw_bounding_boxes(frame: np.ndarray, results: Results,
                        model: YOLO) -> np.ndarray:
    """
    Рисует ограничивающие рамки вокруг обнаруженных объектов на кадре.
    Параметры:
    - frame: Кадр видео для рисования рамок.
    - results: Результаты детекции модели.
    - model: Экземпляр модели YOLO.
    """
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    classes = results[0].boxes.cls.cpu().numpy().astype(int)
    scores = results[0].boxes.conf.cpu().numpy()

    for box, clss, score in zip(boxes, classes, scores):
        if score > 0.5:
            random.seed(int(clss) + 8)
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 4)
            cv2.putText(
                frame,
                f"{model.model.names[clss]}",
                (box[0], box[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (50, 255, 50),
                3,
            )  # pylint: disable=no-member

    return frame


def process_video(video_file: str, model: YOLO) -> None:
    """
    Обрабатывает видео, используя модель для детекции объектов.
    Параметры:
    - video_file: Путь к файлу видео.
    - yolo_model_current: Экземпляр модели YOLO для обработки видео.
    """
    cap = cv2.VideoCapture(video_file)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        if results[0].boxes is not None:
            draw_bounding_boxes(frame, results, model)

        stframe.image(frame, channels="BGR", use_column_width=True)
    cap.release()


def download_youtube_video(url: str) -> str:
    """
    Скачивает видео с YouTube по указанной ссылке.
    Параметры:
    - url: URL-адрес видео на YouTube.
    """
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension="mp4").first()
        temp_dir = tempfile.mkdtemp()
        video_path = stream.download(output_path=temp_dir)
        return video_path
    except AgeRestrictedError:
        st.error(f"Видео '{url}'"
                 f" ограничено по возрасту и не может быть загружено.")
        return None


if __name__ == "__main__":
    # Скачивание модели и её загрузка
    download_file(MODEL_URL, MODEL_DESTINATION)
    yolo_model = YOLO(MODEL_DESTINATION)

    # Создание интерфейса Streamlit
    st.title("Детекция дорожных знаков на видео")

    # Ввод ссылки на YouTube
    youtube_url = st.text_input("Вставьте ссылку на YouTube видео")

    # Элемент загрузки файла
    uploaded_file = st.file_uploader("Или загрузите видео файл", type=["mp4", "avi"])

    # Обработка YouTube URL
    if youtube_url:
        with st.spinner("Скачиваем видео..."):
            video_file_path = download_youtube_video(youtube_url)
            if video_file_path is not None:
                st.success("Видео скачано!")
                process_video(video_file_path, yolo_model)
                os.remove(video_file_path)
            else:
                st.error("Не удалось скачать видео.")

    # Обработка загруженного файла
    elif uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tfile:
            tfile.write(uploaded_file.read())
            process_video(tfile.name, yolo_model)

