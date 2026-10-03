import gzip
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

from shared.logger import logging
from shared.env import settings

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = "Create a compressed PostgreSQL database backup"

    def handle(self, *args, **options):
        backup_dir = Path(settings.BACKUP_DIR)
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.sql.gz"

        dump_command = [
            "pg_dump",
            "--host",
            settings.DB_HOST,
            "--port",
            str(settings.DB_PORT),
            "--username",
            settings.DB_USER,
            "--dbname",
            settings.DB_NAME,
            "--no-password",
        ]

        try:
            self.stdout.write("Creating database backup...")

            process = subprocess.Popen(
                dump_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={
                    **os.environ,
                    "PGPASSWORD": settings.DB_PASSWORD,
                },
            )

            with gzip.open(backup_file, "wb") as compressed_file:
                while chunk := process.stdout.read(8192):
                    compressed_file.write(chunk)

            stderr = process.stderr.read().decode()
            return_code = process.wait()

            if return_code != 0:
                if backup_file.exists():
                    backup_file.unlink()

                raise CommandError(
                    f"Database backup failed: {stderr.strip()}"
                )

            self.verify_backup(backup_file)

            file_size = backup_file.stat().st_size

            logger.info(
                "Database backup completed successfully: %s (%d bytes)",
                backup_file,
                file_size,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Database backup completed: {backup_file}"
                )
            )

            self.cleanup_old_backups(backup_dir)

        except FileNotFoundError:
            raise CommandError(
                "pg_dump was not found. Make sure PostgreSQL client is "
                "installed and pg_dump is available in PATH."
            )

    @staticmethod
    def verify_backup(backup_file: Path) -> None:
        if not backup_file.exists():
            raise CommandError(
                "Database backup failed: backup file was not created."
            )

        if backup_file.stat().st_size == 0:
            backup_file.unlink()
            raise CommandError(
                "Database backup failed: backup file is empty."
            )

        try:
            with gzip.open(backup_file, "rb") as compressed_file:
                compressed_file.read(1)
        except (OSError, EOFError):
            backup_file.unlink()
            raise CommandError(
                "Database backup failed: invalid gzip file."
            )

    @staticmethod
    def cleanup_old_backups(backup_dir: Path) -> None:
        retention_days = settings.BACKUP_RETENTION_DAYS
        cutoff_time = datetime.now() - timedelta(days=retention_days)

        for backup_file in backup_dir.glob("backup_*.sql.gz"):
            modified_time = datetime.fromtimestamp(
                backup_file.stat().st_mtime
            )

            if modified_time < cutoff_time:
                backup_file.unlink()

                logger.info(
                    "Deleted expired database backup: %s",
                    backup_file,
                )