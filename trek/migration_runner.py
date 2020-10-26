from os import name
from .database_providers import SqlServerDatabaseProvider
from .file_manager import FileManager
from .logger import logger
from .migration_manager import MigrationManager
from .models import NEW_MIGRATION


class MigrationRunner:

    def __init__(self, project_path):
        self.logger = logger
        # self.logger = self.logger.bind(path=project_path)
        self.file_manager = FileManager(project_path)
        self.migration_manager = MigrationManager(project_path)
        self.manifest = self.migration_manager.manifest

        self.database_provider = SqlServerDatabaseProvider()

    def _get_applied_migrations(self):
        return self.database_provider.get_applied_migrations()

    def plan(self):
        self.database_provider.setup_migrations_table()

        self.logger.info("Determining which items to migrate")
        db_applied_migrations = self._get_applied_migrations()
        migration = NEW_MIGRATION.copy()
        migration['name'] = 'test migration'
        migration_valid = False

        for m in self.manifest['migrations']:
            if m['name'] not in db_applied_migrations:
                self.logger.info(
                    "Migration has not been applied", name=m['name'])

        for k in migration['files'].keys():

            scripts = self.manifest['files'][k]
            scripts_applied = []

            for m in self.manifest['migrations']:
                scripts_applied += m['files'][k]

            scripts = sorted(scripts)
            scripts_to_apply = []

            for s in scripts:
                if s not in scripts_applied:
                    scripts_to_apply.append(s)

            if scripts_to_apply:
                migration_valid = True

            migration['files'][k] = scripts_to_apply

        if(migration_valid):
            self.migration_manager.append_migration_to_manifest(migration)

            self.logger.info("Migration has been planned.")

            self.logger.info(
                "Look at the manifest to see which scripts will be run")

    def apply(self):

        # -- ensure that the migrations are ready to be applied
        self.database_provider.setup_migrations_table()

        # -- what migrations have been applied?
        migrations_applied = self._get_applied_migrations()

        for m in self.manifest['migrations']:

            if m['name'] not in migrations_applied:
                self.logger.info("Migration will be applied", name=m['name'])

                applied_scipts = {}
                try:
                    for k, v in m['files'].items():
                        for f in v:
                            self.logger.info("Applying script", script=f)
                            text = self.file_manager.get_script_text(f, k)

                            self.database_provider.apply_migration_script(text)
                            applied_scipts[k] = f

                    self.database_provider.apply_migration(m['name'])
                except:
                    self.logger.error("Migration failed to apply.. ")
                    self.logger.info("Rolling back")

                    # if the migration fails midway, roll back the migration
                    for k, v in applied_scipts.items():
                        index = v.split('_')[0]
                        rollback_file = "{}_BACKWARDS.sql".format(index)
                        text = self.file_manager.get_script_text(
                            rollback_file, k)
                        self.database_provider.apply_migration_script(text)

        self.logger.info(
            "Migrations have been run and your database is up to date! Hooray!")
