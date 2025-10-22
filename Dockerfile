FROM python:3.12.0-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

RUN mkdir -p /app/staticfiles

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "djangoweb.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]