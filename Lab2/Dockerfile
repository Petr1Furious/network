FROM python:3.12.4-bullseye

RUN apt update -y && apt install -y iputils-ping

WORKDIR /app

COPY main.py /app

CMD ["python", "/app/main.py", "-s", "4", "-i", "77.88.55.242"]
