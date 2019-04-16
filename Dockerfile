#x86only FROM debian:testing as qemu

#x86only RUN apt-get update && apt-get install -y \
#x86only     qemu-user-static \
#x86only  && rm -rf /var/lib/apt/lists/*

FROM python:3.4

#x86only COPY --from=qemu /usr/bin/qemu-arm-static /usr/bin

WORKDIR /usr/src/app

COPY requirements.txt patch.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
 && patch -d/usr/local/lib/python3.4/site-packages/soco < patch.txt

COPY . .

CMD [ "python", "./KassetteV2.py" ]
