# Use the official Nginx image
FROM nginx:alpine

# Copy the Nginx configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the Nginx port (default 80)
EXPOSE 80