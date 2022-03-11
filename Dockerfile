FROM python:3.8.1

ENV DATADIR=/opt/app/data/

WORKDIR /opt/app

COPY . .

RUN apt update -y ;\
    apt install nginx -y;\ 
    pip install --no-cache-dir -r requirements.txt;\
    python3 -m spacy download en_core_web_lg;\
    cat /etc/os-release;

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
