FROM archlinux/base
MAINTAINER Lars Heinemann

RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm gcc git python python-pip nodejs yarn npm nano nginx

WORKDIR /app
RUN git clone https://github.com/lhein/build-dashboard.git
RUN pip install -r build-dashboard/requirements.txt

WORKDIR /app/build-dashboard
RUN npm install yarn
RUN yarn
RUN yarn build

COPY ./nginx.conf /etc/nginx/nginx.conf
RUN chmod -R a+rwx /app/build-dashboard &&\
    chmod +x /app/build-dashboard/startService.sh
RUN cp -R dist/* /usr/share/nginx/html/

RUN mkdir -p /var/lib/nginx/client-body
RUN mkdir -p /var/lib/nginx/fastcgi
RUN mkdir -p /var/lib/nginx/proxy
RUN mkdir -p /var/lib/nginx/scgi
RUN mkdir -p /var/lib/nginx/uwsgi
RUN chown -R http:root /var/lib/nginx
RUN mkdir -p /var/log/nginx
RUN touch /var/log/nginx/access.log

EXPOSE 80 9000 443 50005

ENV LANG=en_US.UTF-8 \
	GITHUB_TRAVIS_TOKEN=secret

CMD sh ./startService.sh
