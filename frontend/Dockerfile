FROM nginx:alpine

# Copy the static files to the nginx html directory
COPY public/ /usr/share/nginx/html/

# Copy custom nginx configuration if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 