from django.core.management.base import BaseCommand

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.file import FileUtils
import os

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Run Setup"
    working_dir = None
    settings = None
    env = None
    type = None
    utils_version = None
    config = {}

    def __init__(self):
        self.config = self.getConfig()
        self.setWorkingDir()

    def getConfig(self):
        return {}

    def setWorkingDir(self):
        system = System()
        system.cmdExec("pwd", True)
        self.working_dir = system.getCmdExecOutput()

    def add_arguments(self, parser):
        parser.add_argument(
            "--env",
            type=str,
            help="Fixture Environment - kubefacets, development, test",
        ),
        parser.add_argument(
            "--type",
            type=str,
            help="setup or data",
        )
        parser.add_argument(
            "--utils_version",
            type=str,
            help="setup or data",
        )

    def rm_db(self):
        FileUtils.rm_file("db.sqlite3")

    def update_req_file(self):
        filePath = "requirements.txt"
        requirements = FileUtils.read(filePath)
        requirements = [req for req in requirements if not req.startswith("kfsd")]
        requirements.append("kfsd=={}".format(self.utils_version))
        requirementsStr = "\n".join(requirements)
        FileUtils.write(filePath, requirementsStr)

    def update_utils_pkg(self):
        if self.utils_version:
            self.update_req_file()
            cmds = ["pip install -r requirements.txt"]
            System().cmdsExec(cmds, False)

    def clean_db(self):
        system = System()
        self.rm_db()
        if self.utils_version:
            migrationsDir = FileUtils.construct_path(
                self.working_dir, "kubefacets/apps/backend/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)

            kfsdMigrationsDir = FileUtils.construct_path(
                self.working_dir,
                "py_env/lib/python3.10/site-packages/kfsd/apps/models/migrations",
            )
            FileUtils.rm_dir(kfsdMigrationsDir)
            FileUtils.create_dir(kfsdMigrationsDir)
            cmds = [
                "touch {}/__init__.py".format(migrationsDir),
                "touch {}/__init__.py".format(kfsdMigrationsDir),
            ]
            system.cmdsExec(cmds, False)
        else:
            migrationsDir = FileUtils.construct_path(
                self.working_dir, "kfsd/apps/models/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)
            cmd = "touch {}/__init__.py".format(migrationsDir)
            system.cmdExec(cmd, False)

    def run(self):
        fileFormat = ""
        config = self.config[self.env]
        envs = config["env"]

        system = System()

        for k, v in envs.items():
            os.environ[k] = v
            fileFormat += "export {}={}\n".format(k, v)

        if self.type == "cleanup":
            fns = config[self.type]
            [fn() for fn in fns]
        elif self.type in ["server", "msmq", "exec"]:
            serverCmd = config[self.type]
            cmd = "{} --settings={}".format(serverCmd, self.settings)
            fileFormat += "{}\n".format(cmd)
            FileUtils.write("{}.sh".format(self.type), fileFormat)
        elif self.type == "migrate":
            cmds = config[self.type]
            for cmd in cmds:
                system.cmdExec("{} --settings={}".format(cmd, self.settings), False)
        else:
            fixtures = config[self.type]
            cmds = [
                "python manage.py loaddata {} --settings={}".format(
                    fixture, self.settings
                )
                for fixture in fixtures
            ]

            for cmd in cmds:
                system.cmdExec(cmd, False)

    def handle(self, *args, **options):
        self.env = DictUtils.get(options, "env")
        self.type = DictUtils.get(options, "type")
        self.settings = DictUtils.get(options, "settings")
        self.utils_version = DictUtils.get(options, "utils_version", None)
        logger.info("Running setup for env: {}, type: {}".format(self.env, self.type))
        self.run()
