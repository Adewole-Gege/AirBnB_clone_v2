#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""
from fabric.api import put, run, env
import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.hosts = ["54.144.138.231", "34.201.61.21"]


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive to deploy

    Returns:
        bool: True if all operations have been done correctly, False otherwise
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist")
        return False
    try:
        # Extract archive name and target folder name
        archive_name = archive_path.split("/")[-1]
        folder_name = f"/data/web_static/releases/{archive_name.split('.')[0]}"

        # Upload the archive to /tmp/ on the servers
        put(archive_path, f"/tmp/{archive_name}")

        # Create the target directory on the servers
        run(f"mkdir -p {folder_name}")

        # Uncompress the archive into the target directory
        run(f"tar -xzf /tmp/{archive_name} -C {folder_name}")

        # Remove the archive from /tmp/ on the servers
        run(f"rm /tmp/{archive_name}")

        # If a web_static folder exists inside the extracted folder,
        # move its contents to the parent folder and remove it.
        if run(f"test -d {folder_name}/web_static", warn_only=True).succeeded:
            run(f"mv {folder_name}/web_static/* {folder_name}/")
            run(f"rm -rf {folder_name}/web_static")

        # Remove the existing symbolic link, if it exists (warn only to avoid errors)
        run("rm -rf /data/web_static/current", warn=True)

        # Create a new symbolic link linking to the new deployment
        run(f"ln -s {folder_name} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error during deployment:", e)
        return False
