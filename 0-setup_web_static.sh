#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static:
#  - Installs Nginx if not already installed
#  - Creates the required directory structure in /data/
#  - Generates a fake HTML file to test the Nginx configuration
#  - Creates (or recreates) a symbolic link to the test folder
#  - Changes ownership of /data/ to the ubuntu user and group (recursively)
#  - Updates the Nginx configuration so that Nginx serves the content of
#    /data/web_static/current/ when accessing /hbnb_static using an alias
#  - Restarts Nginx so that the configuration changes take effect

set -e

###############################
# 1. Install Nginx if needed
###############################
apt-get update -y
apt-get install -y nginx

#############################################
# 2. Create the folder structure if not exists
#############################################
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

######################################################
# 3. Create a fake HTML file to test Nginx configuration
######################################################
cat > /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
ALX
  </body>
</html>
EOF

############################################
# 4. Create (or recreate) the symbolic link
############################################
rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

#########################################################
# 5. Change ownership of /data/ to ubuntu:ubuntu recursively
#########################################################
chown -R ubuntu:ubuntu /data/

######################################################################
# 6. Update Nginx configuration to serve /data/web_static/current/ at /hbnb_static
######################################################################
NGINX_CONF="/etc/nginx/sites-available/default"

# Remove any previous /hbnb_static/ location block if present.
sed -i '/location \/hbnb_static\/ {/,/}/d' "$NGINX_CONF"

# Insert the location block inside the server block.
# Using ANSI-C quoting ($'…') allows us to include newline (\n) and tab (\t) escape sequences.
if ! grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    sed -i $'s/server {/\0\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n/' "$NGINX_CONF"
fi

#########################################
# 7. Restart Nginx to apply configuration
#########################################
service nginx restart

exit 0
