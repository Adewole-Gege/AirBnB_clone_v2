#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
"""
from fabric.api import env, run, local

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    Args:
        number: the number of archives to keep (default 0)
    """
    number = int(number)
    if number <= 1:
        number = 1

    # Delete local archives
    local_archives = local("ls -t versions", capture=True).split("\n")
    for archive in local_archives[number:]:
        local(f"rm -rf versions/{archive}")

    # Delete remote archives
    remote_archives = run("ls -t /data/web_static/releases").split("\n")
    for archive in remote_archives[number:]:
        if "web_static_" in archive:
            run(f"rm -rf /data/web_static/releases/{archive}")
