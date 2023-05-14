# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.0
ENV PYTHONUNBUFFERED=1
RUN mkdir /ML_app
WORKDIR /ML_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT [ "./docker-entrypoint.sh" ]
#FROM python:3.8
#
## create root directory for our project in the container
#RUN mkdir /ML_app
#
## Set the working directory to /ML_app
#WORKDIR /ML_app
#
## Copy the current directory contents into the container at /music_service
#ADD  . /ML_app/
## Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt
#
#EXPOSE 8000
#CMD ["python", "manage.py", "collectstatic"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]