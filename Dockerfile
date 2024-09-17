FROM python:3.11.0
ENV PYTHONUNBUFFERED 1

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
# ENTRYPOINT [ "/app/django.sh" ]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]