#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static:
# - Installs Nginx if needed
# - Creates the folder structure required
# - Generates a fake HTML file to test Nginx configuration
# - Creates (or recreates) a symbolic link to the test folder
# - Changes ownership of /data/ to the ubuntu user:group
# - Updates Nginx configuration to serve the content at /hbnb_static

# Update package list and install Nginx if not already installed
apt-get update -y
apt-get install -y nginx

# Create required directories (if they do not already exist)
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

# Delete the symbolic link if it already exists and create a new one
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current/ when accessing /hbnb_static
# The following sed command inserts the location block after the line containing "server {"
sed -i '/server {/a \
\n\tlocation /hbnb_static/ {\
\n\t\talias /data/web_static/current/;\
\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply the new configuration
service nginx restart

# Exit successfully
exit 0
