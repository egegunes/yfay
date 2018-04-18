FROM alpine:latest
ADD requirements.txt ./
ADD yfay.py ./
ADD crontab ./
RUN apk add --update python3 py-pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN /usr/bin/crontab /crontab

CMD /usr/sbin/crond -f -l 8

