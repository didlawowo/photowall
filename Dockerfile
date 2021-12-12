
FROM python:3.10-slim
RUN mkdir /photowall
WORKDIR /photowall
COPY . .

RUN pipenv install


EXPOSE 8080
CMD ["python", "app.py"]
