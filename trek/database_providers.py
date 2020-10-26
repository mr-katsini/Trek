

from types import resolve_bases
import pyodbc


class DatabaseProvider(object):
    pass


class SqlServerDatabaseProvider(DatabaseProvider):

    def __init__(self):

        # -- TODO: Thse should come from config of some kind
        # ps: This is a db on my localbox.
        self.username = "sa"
        self.password = "Password!1"
        self.host = "localhost"
        self.db_name = "Dough"
        self.driver = "{ODBC Driver 17 for SQL Server}"

    @property
    def connection_string(self):

        return "Driver={};Server={};DATABASE={};UID={};PWD={}".format(
            self.driver,
            self.host,
            self.db_name,
            self.username,
            self.password
        )

    def test_connection(self):
        conn = pyodbc.connect(self.connection_string)
        conn.close()

    def setup_migrations_table(self):

        # TODO: Support different database engines and ensure sql is compatible
        query = """
        IF  NOT EXISTS (SELECT * FROM sys.objects 
        WHERE object_id = OBJECT_ID(N'[dbo].[__Migrations]') AND type in (N'U'))

        BEGIN
            CREATE TABLE __Migrations(
                [Name] VARCHAR(100) PRIMARY KEY,
                [DateApplied] DATETIME DEFAULT(GETDATE())
            );
        END
        """
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.commit()
        cursor.close()

    def apply_migration_script(self, migration_text):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute(migration_text)
        cursor.commit()
        cursor.close()

    def apply_migration(self, name):
        query = """
            INSERT INTO __Migrations
            ([Name])
            VALUES
            ('{}')
        """.format(name)
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.commit()
        cursor.close()

    def get_applied_migrations(self):

        # TODO: this should be engine agnostic.
        query = "SELECT Name from __Migrations;"

        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute(query)

        result = []
        for r in cursor:
            result.append(r[0])

        cursor.close()

        return result
