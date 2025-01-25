#!/usr/bin/env bash
# Script to set up web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt update
sudo apt install -y nginx

# Create required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a simple HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    ALX School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link, replacing it if it exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current to /hbnb_static
sudo sed -i "/server_name _;/a \\
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart
