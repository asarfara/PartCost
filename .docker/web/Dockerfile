FROM python:3.5

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor cron

RUN pip3 install uwsgi

COPY . /opt/projects/

RUN pip3 install -r /opt/projects/requirements.txt

RUN useradd --no-create-home nginx

RUN chmod 755 $(find /opt/projects/ -type d)
RUN chmod 644 $(find /opt/projects/ -type f)
RUN chown nginx:nginx /opt/projects/ -R

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY ./.docker/web/config/nginx.conf /etc/nginx/
COPY ./.docker/web/config/flask-site-nginx.conf /etc/nginx/conf.d/
COPY ./.docker/web/config/uwsgi.ini /etc/uwsgi/
COPY ./.docker/web/config/supervisord.conf /etc/
COPY ./.docker/web/config/project-cron /etc/cron.d/

RUN service cron restart

WORKDIR /opt/projects

CMD ["/usr/bin/supervisord"]