FROM python:3.11.2-slim
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . ./
CMD gunicorn -b 0.0.0.0:80 app:server