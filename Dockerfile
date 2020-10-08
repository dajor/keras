#FROM python:3.8
FROM tensorflow/tensorflow:latest
WORKDIR /app
COPY requirements.txt /app
RUN pip install cmake

RUN pip install -r ./requirements.txt
RUN apt install -y tesseract-ocr poppler-utils libxext-dev libsm-dev libxrender-dev
#RUN pip install tensorflow
RUN pip install pdf2image
RUN pip install datefinder
RUN pip install pytesseract
ADD . /app
COPY . /app
CMD ["python", "manage.py", "runserver" , "--host", "0.0.0.0"]