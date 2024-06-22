FROM python:3.12.4-bullseye

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app

CMD ["python", "/app/main.py", "-i", "77.88.55.242"]
