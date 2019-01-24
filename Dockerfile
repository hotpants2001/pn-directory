FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn pnapp.wsgi:application --bind 0.0.0.0:$PORT --workers 2
