FROM python:3.8.0
ENV PYTHONUNBUFFERED=1
RUN mkdir /ML_app
WORKDIR /ML_app
ADD  . /ML_app/
RUN pip3 install -r requirements.txt
RUN ["chmod", "+x", "docker-entrypoint.sh"]
CMD [ "./docker-entrypoint.sh" ]

