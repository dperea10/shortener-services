FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update && apt-get install -y mongodb-org

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pymongo

COPY ./main.py /app/

RUN apt-get update && \
    apt-get install -y nginx && \
    rm /etc/nginx/sites-enabled/default && \
    rm /etc/nginx/nginx.conf

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/servers.conf /etc/nginx/servers.conf
COPY nginx /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app

ENV PYTHONUNBUFFERED=TRUE
ENV PORT=8000
ENV MONGODB_HOST=mongodb1
ENV MONGODB_PORT=27017
# CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--reload", "--bind", "0.0.0.0:8000"]
# CMD mongod --bind_ip 0.0.0.0 && uvicorn main:app --reload  
CMD mongod --bind_ip 0.0.0.0 && exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --worker-class uvicorn.workers.UvicornWorker --reload --timeout 120 main:appx
EXPOSE $PORT