FROM python:3.6-slim
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./data /deploy/data/
COPY ./tools /deploy/tools/
COPY ./vosk-model-small-ru-0.22 /deploy/vosk-model-small-ru-0.22/
COPY ./templates/upload.html /deploy/templates/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]