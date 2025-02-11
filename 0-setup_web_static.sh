#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static:
#  - Installs Nginx if not already installed
#  - Creates the folder structure to deploy web_static
#  - Creates a fake HTML file to test the Nginx configuration
#  - Creates (or recreates) a symbolic link to the test folder
#  - Changes ownership of the /data/ folder to the ubuntu user and group
#  - Updates Nginx configuration to serve the content of /data/web_static/current/ at /hbnb_static

# Exit immediately if a command exits with a non-zero status
set -e

# Install Nginx if not installed, and update the package list
apt-get update -y
apt-get install -y nginx

# Create required directories (if they don't already exist)
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
cat <<EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>
EOF

# Delete existing symbolic link if it exists and create a new one
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Define the Nginx default configuration file
NGINX_CONF="/etc/nginx/sites-available/default"

# Check if the configuration already contains the location block
if ! grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    # Insert the location block inside the server block.
    # The following sed command looks for the first occurrence of "server {" and appends the location block right after it.
    sed -i '/server {/a \
    \tlocation /hbnb_static/ {\
    \n\t\talias /data/web_static/current/;\
    \n\t}' "$NGINX_CONF"
fi

# Restart Nginx to apply the configuration changes
service nginx restart

# Exit successfully
exit 0
