FROM python:3.9-alpine
WORKDIR /backend
COPY requirements.txt .
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN pip install -r requirements.txt
EXPOSE 8000
COPY  . .
CMD python manage.py runserver 0.0.0.0:8000