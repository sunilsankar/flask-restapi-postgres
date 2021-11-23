FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD ["python3", "app.py"]
#RUN chmod u+x ./entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]
ENV FLASK_APP=app.py
#CMD flask db migrate && flask db upgrade && flask run -h 0.0.0.0 -p 5000
CMD flask run -h 0.0.0.0 -p 5000
