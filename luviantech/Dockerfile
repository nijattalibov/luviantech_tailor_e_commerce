FROM python:3.8.6
ENV PYTHONUNBUFFERED 1
ENV DEBUG False
WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
gettext 
# RUN celery -A dost_report worker --beat --scheduler django --loglevel=info

COPY . .


# CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]

CMD [ "gunicorn", "--bind", "0.0.0.0", "-p", "8000",  "luviantech.wsgi" ]