
FROM python:3.10-slim
RUN mkdir /photowall
WORKDIR /photowall
COPY . .

RUN pip install -r requirements.txt \
 && rm -rf requirements.txt


EXPOSE 8080
CMD ["python", "app.py"]
