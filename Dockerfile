FROM python:3-alpine
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "/app/app.py"]