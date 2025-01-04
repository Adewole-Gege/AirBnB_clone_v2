import os
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

# Determine the storage type from environment variable
storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

# Reload storage to initialize data
storage.reload()
