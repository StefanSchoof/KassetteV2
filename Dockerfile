FROM python:3.4

WORKDIR /usr/src/app

COPY requirements.txt patch.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
 && patch -d/usr/local/lib/python3.4/site-packages/soco < patch.txt

COPY . .

CMD [ "python", "./KassetteV2.py" ]
