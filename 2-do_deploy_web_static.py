#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import env, put, run
import os

env.hosts = ['54.144.138.231', '34.201.61.21']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    Returns True if successful, otherwise False
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name_no_ext = file_name.split(".")[0]
        remote_path = f"/data/web_static/releases/{name_no_ext}/"
        put(archive_path, "/tmp/")
        run(f"mkdir -p {remote_path}")
        run(f"tar -xzf /tmp/{file_name} -C {remote_path}")
        run(f"rm /tmp/{file_name}")
        run(f"mv {remote_path}web_static/* {remote_path}")
        run(f"rm -rf {remote_path}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {remote_path} /data/web_static/current")
        return True
    except:
        return False
