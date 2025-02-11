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
        bool: True if all operations have been done correctly,
              False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    # Extract archive name and folder name.
    archive_name = archive_path.split("/")[-1]
    folder = archive_name.split(".")[0]
    folder_name = "/data/web_static/releases/" + folder

    # Upload the archive to /tmp/ on the servers.
    result = put(archive_path, "/tmp/" + archive_name)
    if result.failed:
        return False

    # Create the target directory on the servers.
    result = run("mkdir -p " + folder_name)
    if result.failed:
        return False

    # Uncompress the archive into the target directory.
    tar_cmd = ("tar -xzf /tmp/" + archive_name +
               " -C " + folder_name)
    result = run(tar_cmd)
    if result.failed:
        return False

    # Remove the archive from /tmp/ on the servers.
    result = run("rm /tmp/" + archive_name)
    if result.failed:
        return False

    # If the extracted folder contains a web_static directory,
    # move its contents to the parent folder.
    result = run("test -d " + folder_name + "/web_static", warn_only=True)
    if result.succeeded:
        result = run("mv " + folder_name + "/web_static/* " + folder_name + "/")
        if result.failed:
            return False
        result = run("rm -rf " + folder_name + "/web_static")
        if result.failed:
            return False

    # Remove the existing symbolic link; force a 0 exit code.
    run("rm -rf /data/web_static/current || true", warn_only=True)

    # Create a new symbolic link.
    result = run("ln -s " + folder_name +
                 " /data/web_static/current")
    if result.failed:
        return False

    return True
