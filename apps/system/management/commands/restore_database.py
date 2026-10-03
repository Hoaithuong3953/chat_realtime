import gzip
import os
import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

from shared.env import settings
from shared.logger import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = "Restore a compressed PostgreSQL database backup"

    def add_arguments(self, parser):
        parser.add_argument(
            "backup_file",
            type=str,
            help="Path to the .sql.gz backup file",
        )
        parser.add_argument(
            "database_name",
            type=str,
            help="Target PostgreSQL database name",
        )

    def handle(self, *args, **options):
        backup_file = Path(options["backup_file"])
        database_name = options["database_name"]

        if not backup_file.exists():
            raise CommandError(
                f"Backup file not found: {backup_file}"
            )

        if backup_file.suffixes != [".sql", ".gz"]:
            raise CommandError(
                "Backup file must have .sql.gz extension."
            )

        restore_command = [
            "psql",
            "--host",
            settings.DB_HOST,
            "--port",
            str(settings.DB_PORT),
            "--username",
            settings.DB_USER,
            "--dbname",
            database_name,
            "--no-password",
        ]

        self.stdout.write(
            f"Restoring backup to database '{database_name}'..."
        )

        try:
            process = subprocess.Popen(
                restore_command,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={
                    **os.environ,
                    "PGPASSWORD": settings.DB_PASSWORD,
                },
            )

            with gzip.open(backup_file, "rb") as compressed_file:
                while chunk := compressed_file.read(8192):
                    process.stdin.write(chunk)

            process.stdin.close()

            stderr = process.stderr.read().decode()
            return_code = process.wait()

            if return_code != 0:
                raise CommandError(
                    f"Database restore failed: {stderr.strip()}"
                )

            logger.info(
                "Database restore completed successfully: %s -> %s",
                backup_file,
                database_name,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Database restore completed: {database_name}"
                )
            )

        except FileNotFoundError:
            raise CommandError(
                "psql was not found. Make sure PostgreSQL client is "
                "installed and psql is available in PATH."
            )