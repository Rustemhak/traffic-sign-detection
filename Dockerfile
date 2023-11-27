COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
