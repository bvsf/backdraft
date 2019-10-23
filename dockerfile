# start from an official image
FROM python:3.6

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/backdraft
WORKDIR /opt/services/backdraft

# copy our project code
COPY . /opt/services/backdraft

# install our two dependencies
RUN pip install -r requirements.txt

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sigcaw.wsgi:application"]
