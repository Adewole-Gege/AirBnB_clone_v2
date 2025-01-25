#!/usr/bin/env bash
# Set up the server for deployment of web_static

sudo apt-get update -y
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html><body><h1>ALX</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/^\s*location \/ {/a \ \tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo systemctl restart nginx
exit 0
