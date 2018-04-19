FROM alpine:latest
ADD requirements.txt ./
ADD yfay.py ./
ADD crontab ./
RUN apk add --update python3
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r /requirements.txt
RUN /usr/bin/crontab /crontab

CMD /usr/sbin/crond -f -l 8

