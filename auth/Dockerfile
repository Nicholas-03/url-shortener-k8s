FROM python:3.8

WORKDIR /usr/src/app/Auth

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "./app.py"]