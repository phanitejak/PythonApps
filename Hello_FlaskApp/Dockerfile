FROM centos:latest

MAINTAINER PhanitejaK "kondapalliphaniteja@gmail.com"

RUN yum update -y && yum install -y --skip-broken nginx vim python3*

COPY ./requirements.txt /requirements.txt
COPY nginx.default /etc/nginx/sites-available/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 5001
STOPSIGNAL SIGTERM

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ]