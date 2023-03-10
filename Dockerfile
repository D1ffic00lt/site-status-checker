FROM python:3.10.4-slim

COPY requirements.txt requirements.txt

EXPOSE 0:65535

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]