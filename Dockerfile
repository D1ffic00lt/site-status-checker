FROM python:3.10

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY checker checker
COPY .gitignore .gitignore
COPY app.py app.py
COPY README.md README.md
COPY requirements.txt requirements.txt

CMD [ "python", "app.py" ]