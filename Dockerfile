FROM python:3.7
COPY ./requirements.txt ./flask_wrap.py ./start_service.sh ./example.py /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./start_service.sh"]
#ENTRYPOINT ["/bin/bash"]


