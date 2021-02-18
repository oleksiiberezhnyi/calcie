FROM python:3.9.1-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
#RUN mkdir -p /opt/app/api /opt/app/config
#COPY requirements.txt /opt/app
#RUN pip install -r /opt/app/requirements.txt
#ARG ENVIRONMENT
#COPY api /opt/app/api
#COPY config/gunicorn.local.py /opt/app/config/gunicorn_config.py
#ENV PYTHONPATH /opt/app
#WORKDIR /opt/app
#CMD ["gunicorn", "--reload", "-k", "gevent", "-c", "/opt/app/config/gunicorn_config.py", "./app.py"]