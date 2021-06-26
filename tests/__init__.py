import os
import tempfile
from shutil import copy
from grocery_api.config import GROCERY_TEST_DATABASE, PROJECT_ROOT

dirpath = tempfile.TemporaryDirectory(dir = "/tmp")
copy(f"{PROJECT_ROOT}/{GROCERY_TEST_DATABASE}", dirpath.name)
temp_db_file = f"sqlite:///{dirpath.name}/{GROCERY_TEST_DATABASE}"
os.environ['DATABASE_URI'] = temp_db_file