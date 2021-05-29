FROM python:3.9-alpine

RUN apk add --no-cache py3-libevdev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./KassetteV2.py" ]
