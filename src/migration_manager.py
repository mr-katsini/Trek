from file_manager import FileManager
from models import MIGRATION_MANIFEST
from logger import logger
import json


class MigrationManager:

    def __init__(self, project_path):
        self.logger = logger
        self.logger = self.logger.bind(path=project_path)
        self.file_manager = FileManager(project_path)

    def __pluralize(self, text):
        return "{}s".format(text)

    def __get_file_index(self, type):
        type = self.__pluralize(type)
        index = len(self.manifest['files'][type])
        return format(index + 1, '04')

    @property
    def manifest(self):

        _manifest = self.file_manager.get_migration_manifest()

        if _manifest is None:
            return MIGRATION_MANIFEST

        return _manifest

    def append_migration_to_manifest(self, migration):

        manifest = self.manifest
        manifest['migrations'].append(migration)
        self.file_manager.write_migration_manifest(manifest)

    def __append_file_to_manifest(self, filename, type):

        manifest = self.manifest

        # -- update the manifest with the new file
        manifest['files'][self.__pluralize(
            type)].append(filename)

        self.file_manager.write_migration_manifest(manifest)

    def __get_file_name(self, script_action,  script_type, name, description=""):

        # -- get the file index
        index = self.__get_file_index(script_type)

        if description:
            description = description.replace(' ', '_')
            description = "_{}_".format(description)

        # -- get the file name
        filename = "{}_{}_{}_{}{}.sql".format(
            index, script_action, script_type, name, description
        ).upper()

        return filename

    def __create_script(self, name, script_type, script_action, description=""):
        self.logger.info(
            "Adding Script", name=name,
            script_type=script_type,
            script_action=script_action
        )

        filename = self.__get_file_name(
            script_action, script_type, name, description)

        backwards_name = "{}_BACKWARDS.sql".format(
            self.__get_file_index(script_type))

        self.file_manager.write_file(
            "",
            backwards_name,
            self.__pluralize(script_type)
        )

        # -- write the file to disk
        self.file_manager.write_file(
            "",
            filename,
            self.__pluralize(script_type)
        )

        # -- lastly, update the manifest with the new file
        self.__append_file_to_manifest(filename, script_type)

    def create(self, name, script_type):
        self.__create_script(name, script_type, 'create')

    def drop(self, name, script_type):
        self.__create_script(name, script_type, 'drop')

    def alter(self, name, script_type, description):
        self.__create_script(name, script_type, 'alter', description)

    def init(self):

        # -- scaffold the project
        self.file_manager.create_migration_folders()

        # -- write the migration manifest
        self.file_manager.write_file(
            json.dumps(self.manifest, indent=4),
            "Trek.Manifest.json"
        )
