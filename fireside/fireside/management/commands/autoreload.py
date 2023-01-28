import atexit
import logging
import subprocess
import sys

from django.core.management import BaseCommand
from django.utils import autoreload

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Basic management command which will execute a process using the same
    autoreload mechanism used by the runserver command. Processes run with
    this command will be reloaded when changes are made to source files.

    DO NOT USE THIS IN PRODUCTION

    Examples:
      ./manage.py autoreload -- celery -A <project_name> worker -l info
    """

    help = "Run and auto-reload a process using the default django autoreloader"

    def handle(self, *args, **options):
        self.command = options["command"]
        logger.debug(f"Auto reloading '{self.command}' ...")
        autoreload.run_with_reloader(self.run_process)

    def add_arguments(self, parser):
        parser.add_argument("command", nargs="+")

    def run_process(self):
        process = subprocess.Popen(self.command)
        atexit.register(process.terminate)
        sys.exit(process.wait())
