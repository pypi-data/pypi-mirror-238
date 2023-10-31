import uuid
import os
import shutil
import logging
import tempfile
import atexit
import sys
from georeader.logic.main_helpers import winapi_path

LOGGER = logging.getLogger("__name__")

class DirectoryHelper():
    def __init__(self, *args, **kwargs):
        self.tmp_id = str(uuid.uuid1())
        self.working_dir = None
        atexit.register(self.delete_working_dir)

    def clean_up_files_in_working_dir(self):
        """
            Removes all files and folders from the provided tmp directory
        """
        for filename in os.listdir(self.working_dir):
            file_path = os.path.join(self.working_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                LOGGER.warning('Failed to delete %s. Reason: %s' % (file_path, e), exc_info=True)

    def delete_working_dir(self):
        """remove working dir
        """
        if self.working_dir is not None and os.path.exists(self.working_dir):
            try:
                shutil.rmtree(self.working_dir)
            except OSError as e:
                print(e)
                logging.error("Error: %s - %s." % (e.filename, e.strerror), exc_info=True)

    def create_working_dir(self):
        """
            creates temp directory for tmp files.
        """
        tempdir = tempfile.mkdtemp(prefix=f"{self.tmp_id}-")
        # if sys.platform.startswith('win'):
        #     tempdir = winapi_path(tempdir)
        self.working_dir = tempdir

    def reset_working_dir(self):
        """ Deletes current working dir and creates a new one"""
        self.delete_working_dir()
        self.create_working_dir()