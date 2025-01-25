#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the hosts to deploy to
env.hosts = ['54.144.138.231', '34.201.61.21']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns the archive path or None if it fails
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        filename = archive_path.split("/")[-1]
        folder_name = f"/data/web_static/releases/{filename.split('.')[0]}"

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create a new directory
        run(f"mkdir -p {folder_name}")

        # Extract the archive to the new directory
        run(f"tar -xzf /tmp/{filename} -C {folder_name}")

        # Remove the uploaded archive from the server
        run(f"rm /tmp/{filename}")

        # Move the files to the correct location
        run(f"mv {folder_name}/web_static/* {folder_name}")

        # Remove the extra directory created during extraction
        run(f"rm -rf {folder_name}/web_static")

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {folder_name} /data/web_static/current")

        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
