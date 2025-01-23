#!/usr/bin/env bash
# Script to set up web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt update
sudo apt install -y nginx

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a simple HTML file in the test directory
echo "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the test folder
if [ -L /data/web_static/current ]; then
  sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
nginx_conf="/etc/nginx/sites-available/default"
sudo sed -i "/server_name _;/a \\ \n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }" $nginx_conf

# Restart Nginx
sudo service nginx restart
