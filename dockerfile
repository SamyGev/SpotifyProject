FROM python:3.10.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "/usr/src/app/manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000