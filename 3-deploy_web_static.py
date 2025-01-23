#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""
from fabric.api import env
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy

env.hosts = ['<IP web-01>', '<IP web-02>']

def deploy():
    """
    Creates and distributes an archive to web servers
    Returns True if successful, otherwise False
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
