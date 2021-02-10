FROM python:3.7
COPY requirements.txt /home/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /home/requirements.txt
COPY . /home
EXPOSE 5000
ENTRYPOINT ["python", "/home/run.py" ]