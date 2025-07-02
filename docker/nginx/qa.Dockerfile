FROM nginx:latest
# COPY default.conf /etc/nginx/conf.d/default.conf
# WORKDIR /etc/nginx/templates
COPY default.qa.conf /etc/nginx/templates/nginx.conf.template
COPY maintenance.html /usr/share/nginx/html/maintenance.html