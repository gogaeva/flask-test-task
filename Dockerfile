FROM python:3.10

WORKDIR /flask-test-task

COPY app/ app/
COPY requirements.txt . 
COPY memory_checker.py .
COPY start.sh .

RUN pip3 install -r requirements.txt
EXPOSE 8080/tcp
CMD ["/bin/bash", "start.sh"]
