FROM python:latest
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
RUN pip install -r requirements.txt
CMD "python main.py"