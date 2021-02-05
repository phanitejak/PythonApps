FROM python:3.7
WORKDIR /home/sonblog
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /home/sonblog/
CMD 'python /home/sonblog/run.py'