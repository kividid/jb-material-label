# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:alpine

# If you prefer miniconda:
#FROM continuumio/miniconda3


LABEL Name=jb-material-label Version=0.0.1

# RUN apt-get update -y && \
# apt-get install -y python3-pip python3-dev

# RUN apt-get update && apt-get install -y \
#     curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5\
#     && rm -rf /var/lib/apt/lists/*


# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# RUN apt-get update -y
# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools
# RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
# RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# RUN /bin/bash -c "source ~/.bashrc"
# RUN apt-get install -y unixodbc-dev



WORKDIR /home/label

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY static static
COPY templates templates
COPY main.py models.py boot.sh ./
RUN chmod +x boot.sh

EXPOSE 5000

CMD gunicorn -b :5000 --access-logfile - --error-logfile - main:app



# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "jb-material-label"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m jb-material-label"
