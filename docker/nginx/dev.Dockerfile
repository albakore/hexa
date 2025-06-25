FROM nginx:latest
# COPY default.conf /etc/nginx/conf.d/default.conf
# WORKDIR /etc/nginx/templates
COPY default.dev.conf /etc/nginx/templates/nginx.conf.template