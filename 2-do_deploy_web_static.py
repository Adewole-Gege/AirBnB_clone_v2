#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import put, run, env
import os

env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['54.144.138.231', '34.201.61.21']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    Args:
        archive_path (str): The path to the archive to deploy
    Returns:
        bool: True if all operations have been done correctly, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive name and folder name
        archive_name = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/" + archive_name.split(".")[0]

        # Upload the archive to the /tmp/ directory on the servers
        put(archive_path, "/tmp/")

        # Create the target directory
        run(f"mkdir -p {folder_name}")

        # Uncompress the archive to the target directory
        run(f"tar -xzf /tmp/{archive_name} -C {folder_name}")

        # Remove the archive from the /tmp/ directory
        run(f"rm /tmp/{archive_name}")

        # Move the files from the web_static folder
        run(f"mv {folder_name}/web_static/* {folder_name}/")

        # Remove the now-empty web_static folder
        run(f"rm -rf {folder_name}/web_static")

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version
        run(f"ln -s {folder_name} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
