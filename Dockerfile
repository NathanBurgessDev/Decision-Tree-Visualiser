FROM python:3.9-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn --chdir src --workers 3 --bind=0.0.0.0:80  app:app