FROM httpd:2.4

# Enable required modules
RUN sed -i \
    -e '/LoadModule proxy_module/s/^#//g' \
    -e '/LoadModule proxy_http_module/s/^#//g' \
    -e '/LoadModule rewrite_module/s/^#//g' \
    -e '/LoadModule log_config_module/s/^#//g' \
    /usr/local/apache2/conf/httpd.conf

# Copy Apache configuration
COPY apache.conf /usr/local/apache2/conf/httpd.conf

# Copy your frontend files
COPY ./public/ /usr/local/apache2/htdocs/

# Set permissions
RUN chown -R www-data:www-data /usr/local/apache2/htdocs/

EXPOSE 80