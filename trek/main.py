import argparse
from .migration_manager import MigrationManager
from .configuration import SUPPORTED_SCRIPTS
from .migration_runner import MigrationRunner
from argparse import RawTextHelpFormatter


def get_command_line_args():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    sub_parsers = parser.add_subparsers(
        title="Trek Migrations Tool",
        description="A very poor attempt at database versioning",
        help="Usage",
        dest="parser"
    )

    parser.add_argument(
        "-p",
        "--path",
        dest='path',
        default="."
    )

    # -- Create Parsers
    create_parser = sub_parsers.add_parser(
        "create",
        help="Create a new CREATE migration file"
    )

    drop_parser = sub_parsers.add_parser(
        "drop",
        help="Create a new DROP migration file"
    )

    alter_parser = sub_parsers.add_parser(
        "alter",
        help="Create a new ALTER migration file"
    )

    migrate_parser = sub_parsers.add_parser(
        "migrate",
        help="Perform database migrations"
    )

    migrate_parser.add_argument(
        'action',
        choices=['plan', 'apply', 'rollback'],
        help="""Migration action to apply
        plan: plan the migration and show what will be run\n
        apply: Apply the migration to the database
        rollback: Roll back the migration to an earlier state
        """
    )

    init_parser = sub_parsers.add_parser(
        "init",
        help="Setup a new database project"
    )

    setup_parser = sub_parsers.add_parser("setup")

    parsers = [
        create_parser,
        drop_parser,
        alter_parser,
    ]

    for p in parsers:

        # -- add the type from the supported types
        p.add_argument(
            "type",
            type=str,
            help="Type of database object to work on",
            choices=SUPPORTED_SCRIPTS
        )

        # --add the name of the migration
        p.add_argument("name",  type=str)

    # -- add description to alter parser
    alter_parser.add_argument(
        'description',
        help='A short description of what you are changing'
    )

    # -- parse
    args = parser.parse_args()
    return args


def main():
    args = get_command_line_args()

    migration_manager = MigrationManager(args.path)
    migration_runner = MigrationRunner(args.path)

    if args.parser == "create":
        migration_manager.create(args.name, args.type)

    if args.parser == "drop":
        migration_manager.drop(args.name, args.type)

    if args.parser == "alter":
        migration_manager.alter(args.name, args.type, args.description)

    if args.parser == "migrate":

        if args.action == 'plan':
            migration_runner.plan()

        if args.action == 'apply':
            migration_runner.apply()

    if args.parser == "init":
        migration_manager.init()

    if args.parser == "setup":

        pass


if __name__ == '__main__':
    main()
