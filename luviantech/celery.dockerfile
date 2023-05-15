FROM python:3.8.6

WORKDIR /code

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .






