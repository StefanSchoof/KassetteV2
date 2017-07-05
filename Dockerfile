FROM armhf/python:3.4
RUN pip install soco
RUN pip install applicationinsights
ADD "./KassetteV2.py" "./"

CMD [ "python", "./KassetteV2.py" ]