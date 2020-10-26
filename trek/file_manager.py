import os
import json
from .logger import logger
from .configuration import SUPPORTED_SCRIPTS

MANIFEST_FILENAME = "trek.manifest.json"


class FileManager():

    def __init__(self, path):
        self.base_path = path
        self.working_dir = os.path.join(os.getcwd(), path)
        self.logger = logger.bind(path=self.working_dir)

    def get_migration_manifest(self):
        path = os.path.join(self.working_dir, MANIFEST_FILENAME)

        if os.path.exists(path):

            with open(path, 'r') as f:
                return json.loads(f.read())
        self.logger.warning("There is no manifest")
        return None

    def write_migration_manifest(self, manifest):
        self.logger.info("Updating manifest")
        self.write_file(json.dumps(manifest, indent=4), MANIFEST_FILENAME)

    def write_file(self, content,  fileName, path=""):

        path = os.path.join(self.working_dir, path, fileName)

        with open(path, 'w') as f:
            f.write(content)

        self.logger.info("Wrote file", fileName=fileName, path=path)

    def ensure_directory_exists(self, directory_name):
        directory = os.path.join(self.working_dir, directory_name)

        # create dir if not exists
        if not os.path.exists(directory):
            self.logger.info("Creating Directory", directory=directory_name)
            os.mkdir(directory)
        else:
            self.logger.warning("Directory Exists", directory=directory_name)

    def create_migration_folders(self):
        self.logger.info("Scafolding a migration project")

        for p in SUPPORTED_SCRIPTS:
            self.ensure_directory_exists("{}s".format(p.title()))

    def save_file(self, file_name, file_type):
        pass

    def get_script_text(self, name, script_type):

        path = os.path.join(self.working_dir, script_type.title(), name)

        with(open(path, 'r')) as f:
            return f.read()
