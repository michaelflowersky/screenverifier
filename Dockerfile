FROM ubuntu:22.04

RUN sudo apt install tesseract

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["screenverifier.py" ]