FROM python:3.10-alpine
COPY . ./app
WORKDIR ./app
EXPOSE 80:80
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt