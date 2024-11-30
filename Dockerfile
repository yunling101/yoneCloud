FROM python:3.8-slim-bullseye

WORKDIR /yoneCloud

COPY ./public/dist ./public/static
COPY ./scripts/initialize.sh ./scripts/initialize.sh
COPY ./scripts/initialize_*.py ./scripts/
COPY ./scripts/grafana ./scripts/grafana

COPY ./VERSION .
COPY ./webserver/docker ./webserver/config
COPY ./webserver/webserver ./webserver/webserver
COPY ./webserver/*.py ./webserver
COPY ./webserver/uwsgi.ini ./webserver/uwsgi.ini
COPY ./requirements.txt .

COPY ./docker/supervisord ./supervisord

RUN mkdir -p ./webserver/logs && mkdir -p ./webserver/media
RUN find ./webserver/webserver -type d -name "__pycache__" -exec rm -rf {} +
RUN find . -type f -name ".DS_Store" -exec rm -f {} +
RUN find ./webserver/webserver -type d -name "migrations" | while read dir;do \
    find "$dir" -type f -not -name "__init__.py" -exec rm -f {} +;done

ENV PYTHONUNBUFFERED=1
ENV LANG zh_CN.UTF-8

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update \
    && apt install -y locales gcc default-libmysqlclient-dev nginx curl \
    && apt clean \
    && pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && rm -rf ~/.cache/pip

RUN sed -i '60 d' /etc/nginx/nginx.conf

COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/web.conf
COPY ./docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY --from=yunling101/cmdchannel:latest /opt/cmdChannel /yoneCloud/bin/cmdChannel
ENTRYPOINT ["docker-entrypoint.sh"]

STOPSIGNAL SIGQUIT
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8080