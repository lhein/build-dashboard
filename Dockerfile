FROM archlinux
MAINTAINER Lars Heinemann

RUN pacman -Syyu  --noconfirm
RUN pacman -S  --noconfirm gcc git nano npm nginx yarn python python-pip nodejs

WORKDIR /app
RUN git  clone https://github.com/lhein/build-dashboard.git    build-dashboard
RUN pip install -r build-dashboard/requirements.txt

WORKDIR /app/build-dashboard

RUN npm install yarn
RUN yarn 
RUN yarn build 

COPY ./nginx.conf /etc/nginx/nginx.conf 
RUN chmod -R a+rwx /app/build-dashboard &&\
    chmod +x /app/build-dashboard/startService.sh

RUN cp  -R dist/* /usr/share/nginx/html/ 

RUN mkdir -p /var/lib/nginx/client-body
RUN mkdir -p /var/lib/nginx/fastcgi
RUN mkdir -p /var/lib/nginx/proxy
RUN mkdir -p /var/lib/nginx/scgi
RUN mkdir -p /var/lib/nginx/uwsgi
RUN chown -R http:root /var/lib/nginx

# Forward request logs to Docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
 && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 9000 50005

ENV LANG=en_US.UTF-8

CMD sh ./startService.sh
