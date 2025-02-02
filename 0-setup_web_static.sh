#!/usr/bin/env bash
# Set up web servers for deployment of web_static

# Ensure the script exits on any error
set -e

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update -y
    sudo apt-get install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    ALX School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link, recreate if it exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Set ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content
if ! sudo grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sudo sed -i '/server_name _;/a \\\n    location /hbnb_static {\n        alias /data/web_static/current/;\n        index index.html;\n    }' /etc/nginx/sites-available/default
fi

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
