FROM python:3.6.7-jessie

ENV PYTHONUNBUFFERED 1

RUN mkdir /app  
WORKDIR /app

COPY . .

# RUN apt update && apt install -y libpq-dev
RUN pip install -r service-replication-requirements.txt

WORKDIR /app/app_services_replication
ENTRYPOINT ["python", "message_processor.py"]