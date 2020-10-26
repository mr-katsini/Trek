
# Trek
[![Build Status](https://travis-ci.com/mr-katsini/Trek.svg?branch=main)](https://travis-ci.com/mr-katsini/Trek)

_disclaimer - This was a personal project that was intended to solve a requirement for another personal project_

**Trek** is a database versioning tool for database first projects. Write sql and version it _kinda_ safely.

## Features

- Database Versioning
- Database project scaffolding
- Script Management
- Migration Rollbacks

## Coming Soon (WIPs)

These are some of the ideas that I'll get to over some time.

- Templates for generated scripts
- Support for other database engines
  - Postgres
  - MySQL
  - sqlLite
- Migration targeting (Run all migrations to a certain point)
- Migration Rollbacks (Rollback the database to a different point in time)
- Sanity Checking
  - Determining database objects not defined in the repository
  - Script validation

## Trek Manifest
Trek uses a manifest file in the database project to manage migrations

```
    "files": {
        "tables": [],
        "triggers": [],
        "procedures": [],
        "functions": [],
        "seeds": [],
    },
    "migrations": [
        {
            "name": "",
            "files": {
                "tables": [],
                "triggers": [],
                "procedures": [],
                "functions": [],
                "seeds": [],
            },
        }
    ]
```

| Field                        | Description                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| files                        | This object contains a collection of scripts added in the repository |
| files.tables                 | Array of table scripts added in the repository                       |
| files.triggers               | Array of trigger scripts added in the repository                     |
| files.procedures             | Array of procedure scripts added in the repository                   |
| files.functions              | Array of function scripts added in the repository                    |
| files.seeds                  | Array of seed scripts added in the repository                        |
| migrations                   | Array of migration objects created when running `trek migrate plan`  |
| migraions[].files            | Object of files used for this migration                              |
| migraions[].files.tables     | Array of table scripts that will be applied in this migration        |
| migraions[].files.triggers   | Array of trigger scripts that will be applied in this migration      |
| migraions[].files.procedures | Array of procedure scripts that will be applied in this migration    |
| migraions[].files.functions  | Array of function scripts that will be applied in this migration     |
| migraions[].files.seeds      | Array of seed scripts that will be applied in this migration         |

There is a corresponding table that will get created named `__Migrations` which contains the `DateApplied` and `Name` column. each migration will be inserted into `__Migrations` when applie



## How to use it

_This is a work in progress_

### Setup a database project

```
trek init
```
This will setup your project in the current folder

### Configure your database

_Only SqlServer is supported at this time_

Trek uses environment variables to determine which database to use.

| Name             | Description                               |
| ---------------- | ----------------------------------------- |
| TREK_DB_NAME     | The name of the databaseinstance          |
| TREK_DB_HOST     | Hostname of the database server           |
| TREK_DB_USER     | Username to used for auth when connecting |
| TREK_DB_PASSWORD | password to used for auth when connecting |
| TREK_DB_PASSWORD | password to used for auth when connecting |

You can set this in the command line

```
export TREK_DB_NAME=MyDatabase
```

### Adding new scripts

```
trek <action> <object type> <object name>
```

- <action> can be:
    - create
    - alter
    - drop
- <object type> can be:
    - table
    - trigger
    - procedure
    - function
    - index
    - seed
- <object name> is the name of the database object you're working on

When you create a new script, there will always be a `ROLLBACK` script that will simultaneously created for you. It is essential that your rollback script is correct to the nature of the migration.

For example, if you create a `create` script, it will look like this

```
CREATE TABLE MyTable(
    ...
)
```
The corresponding `ROLLBACK` should look like this

```
DROP TABLE MyTable
```

_Rollbacks should always be the reverse of the forward migration and should aim to undo the migration_

This is important as if something goes wrong in the `trek migrate apply` it will run the rollback for each script it applied.

### Planning Migrations

```
trek migrate plan
```

This will check the scripts you have on disk and assert if they should get applied.

It will also tell you which migrations in the manifest have not been applied against your database.

**This will create a table on your database when you run a plan**

Migration plans get written to the manifest.

### Applying Migrations

```
trek migrate apply
```
This will run the scripts that are planned in the manifest against the db. It will only run scripts for migrations that have not yet been applied. 



## Examples

#### Scaffold a project

```
trek init
```

This will create the following folders as well as a manifest file.


```
./
    /Functions/
    /Procedures/
    /Seeds/
    /Tables/
    /Triggers/
    Trek.Manifest.json

```


#### Creating a new script

```
trek create table MyTestTable
```

This will give you the following

```
./
    /Tables/
        0001_CREATE_TABLE_MYTESTTABLE.sql
        0001_BACKWARDS.sql
```

#### Planning Migrations

This will attempt to discover which scripts have not been added to a migration. It will also check the database and determine which migrations haven't been applied

```
$ trek migrate plan

Determining which items to migrate
Migration has been planned and added to the manifest (trek.manifest.json)
Look at the manifest to see which scripts will be run
```

#### Applying Migrations


## Dependencies

Make sure this is installed if you're using unix

_This was dev'd on a mac, if you're using something else, it might not work as intended. But that goes for the entire app in itself_

```
# Mac OSX
brew install unixodbc

# Linux
apt-get install unixodbc

```

These are also needed for the database driver (MACOS)

```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql mssql-tools
brew install unixodbc
```