FROM python:3.7
RUN apt-get update && \
    apt-get install libpq-dev
COPY ./requirements.txt ./flask_wrap.py ./start_service.sh ./example.py /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install --extra-index-url http://ccde-repository.s3-website-us-east-1.amazonaws.com ccde --trusted-host ccde-repository.s3-website-us-east-1.amazonaws.com 
EXPOSE 8000
ENTRYPOINT ["./start_service.sh"]
#ENTRYPOINT ["/bin/bash"]


