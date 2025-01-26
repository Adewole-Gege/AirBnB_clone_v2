#!/usr/bin/env bash
# Set up web servers for deployment of web_static

# Install Nginx if not already installed
apt-get update
apt-get -y install nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    ALX School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link, recreate if it exists
ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content
sed -i '/server_name _;/a \\\n    location /hbnb_static {\n        alias /data/web_static/current/;\n    }' /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
