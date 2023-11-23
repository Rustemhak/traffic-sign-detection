import random
import streamlit as st
from pytube import YouTube
import cv2
import tempfile
import os
from ultralytics import YOLO
import requests


def download_file(url, destination):
    # Проверка, существует ли файл
    if not os.path.exists(destination):
        response = requests.get(url)
        with open(destination, 'wb') as file:
            file.write(response.content)


url = "https://drive.google.com/uc?export=download&id=1Xkkx1h3Tgjm3Y2xTpmoeMONue7ZGy7rT"
destination = "best_yolo.pt"

download_file(url, destination)

# Загрузка модели Ultralytics
model = YOLO('best_yolo.pt')  # убедитесь, что файл best_yolo.pt находится в правильной директории


def draw_bounding_boxes(frame, results):
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    classes = results[0].boxes.cls.cpu().numpy().astype(int)
    scores = results[0].boxes.conf.cpu().numpy()
    for box, clss, score in zip(boxes, classes, scores):
        # Generate a random color for each object based on its ID
        if score > 0.5:
            random.seed(int(clss) + 8)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3],), color, 4)
            cv2.putText(
                frame,
                f"{model.model.names[clss]}",
                (box[0], box[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (50, 255, 50),
                3,
            )
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

        if results[0].boxes != None:
            # Рендеринг ограничивающих рамок и классов на кадре
            draw_bounding_boxes(frame, results)

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
