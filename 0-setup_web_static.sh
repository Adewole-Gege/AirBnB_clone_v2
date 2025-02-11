#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static:
#  - Installs Nginx if not already installed
#  - Creates the required folder structure in /data/
#  - Creates a fake HTML file at /data/web_static/releases/test/index.html to test Nginx
#  - Creates (or recreates) a symbolic link /data/web_static/current linked to the test folder
#  - Changes ownership of /data/ to the ubuntu user and group (recursively)
#  - Updates the Nginx configuration so that Nginx serves the contents of /data/web_static/current/
#    when accessing /hbnb_static using the alias directive
#  - Restarts Nginx so that the configuration changes take effect

set -e

#############################
# 1. Install Nginx if needed
#############################
apt-get update -y
apt-get install -y nginx

########################################
# 2. Create the folder structure needed
########################################
# mkdir -p will create parent directories as needed.
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

#####################################################
# 3. Create a fake HTML file to test Nginx configuration
#####################################################
cat > /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
ALX
  </body>
</html>
EOF

#####################################################
# 4. Create (or recreate) the symbolic link
#####################################################
# Remove the symbolic link if it exists and create a new one
rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

######################################################################
# 5. Change ownership of /data/ folder to ubuntu user and group (recursively)
######################################################################
chown -R ubuntu:ubuntu /data/

###########################################################################
# 6. Update Nginx configuration to serve /data/web_static/current/ at /hbnb_static
###########################################################################
NGINX_CONF="/etc/nginx/sites-available/default"

# Remove any previous location block for /hbnb_static/ (if present)
# This sed command deletes from a line matching "location /hbnb_static/ {" up to the next "}".
sed -i '/location \/hbnb_static\/ {/,/}/d' "$NGINX_CONF"

# Insert the new location block inside the server block.
# The following sed command finds the first line starting with "server {" and immediately
# appends our location block after it.
if ! grep -q "alias /data/web_static/current/;" "$NGINX_CONF"; then
    sed -i "s|^\s*server {|&\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n|" "$NGINX_CONF"
fi

####################################
# 7. Restart Nginx to apply changes
####################################
service nginx restart

exit 0
