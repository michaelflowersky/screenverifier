FROM ubuntu:22.04

RUN apt update && apt install tesseract-ocr python3 python3-pip -y

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["screenverifier.py" ]