FROM python:alpine3.7
COPY . /app
WORKDIR /app
ENV FLASK_APP=mooder
EXPOSE 5000
RUN pip install -r requirements.txt
RUN flask init-db
CMD ["flask", "run", "--host=0.0.0.0"]

