#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive of the web_static folder
"""
from fabric.api import local
from datetime import datetime
import os


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
    except:
        return None

