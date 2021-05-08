FROM python:3.7
WORKDIR /opt
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["nestor.py"]
