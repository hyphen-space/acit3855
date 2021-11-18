FROM ubuntu:18.04 
LABEL maintainer="ata3@my.bcit.ca" 
RUN apt-get update -y && \ 
    apt-get install -y python3 python3-pip 
         
# We copy just the requirements.txt first to leverage Docker cache 
COPY ./requirements.txt /app/requirements.txt 
#COPY ./create_database_mysql.py /app/create_database_mysql.py
WORKDIR /app 
RUN pip3 install -r requirements.txt 
#RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
#RUN python3 create_database_mysql.py
COPY . /app 
ENTRYPOINT [ "python3" ] 
CMD [ "app.py" ]
