FROM ubuntu:22.04

RUN apt install tesseract-ocr -y

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["screenverifier.py" ]