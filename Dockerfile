FROM python:3.8-alpine

MAINTAINER Saeed
LABEL name="Ad server"

RUN mkdir /usr/src/app/

COPY . /usr/src/app/
WORKDIR /usr/src/app/

EXPOSE 5000

RUN pip install -r requirements.txt
RUN python init_db.py

CMD ["python", "app.py"]