from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from shutil import rmtree
from shutil import copy
from os import chdir
from sys import argv
from json import load
from os import environ
from getpass import getpass
from code import interact
from platform import python_version
import logging
import sys
import os

from platformdirs import user_data_dir
from platformdirs import user_documents_dir
import pandas
import yaml

from labcrawler.analyzers.gitlab_analyzer import GitLabAnalyzer
from labcrawler.gitlab_ci_data_loader import GitLabCIDataLoader
from labcrawler.analyzers.gitlab_analyzer import output_neat

APPNAME = "LabCrawler"
APPAUTHOR = "SteampunkWizard"

SOURCES = ['gitlab']


class Simple:
    pass


class LabCrawlerCLI:

    def __init__(self):
        self.set_logging()
        parser = ArgumentParser()
        parser.add_argument('--workspace')
        commands = parser.add_subparsers(dest='command')
        for command in ['melt', 'load', 'analyze']:
            commands.add_parser(command)
        initparser = commands.add_parser('init')
        initparser.add_argument('--output')
        namespace = parser.parse_args(argv[1:])
        if namespace.workspace:
            self.workspace = Path(namespace.workspace).expanduser()
        else:
            self.workspace = Path(user_data_dir(APPNAME, APPAUTHOR))
        getattr(self, namespace.command)(namespace)

    @staticmethod
    def set_logging():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @property
    def config_path(self):
        return self.workspace / 'labcrawler.json'

    def init(self, namespace):
        self.clear_dir("the LabCrawler workspace", self.workspace)
        self.init_meltano()
        self.init_config(namespace.output)
        self.init_plugins()
        print(f"Remember to edit the config file at\n  {self.config_path}")

    @staticmethod
    def clear_dir(prompt: str, dir: Path):
        if dir.exists():
            if dir.is_dir():
                if not len([f for f in dir.iterdir()]):
                    return
            print(dir)
            confirm = input(f"ABSOLUTELY CERTAIN you want " +
                            "to delete {prompt}? (type YES)? ")
            if confirm != 'YES':
                raise RuntimeError("User cancelled")
            if dir.is_file():
                dir.unlink()
            elif dir.is_dir():
                rmtree(dir)
        dir.mkdir(parents=True)

    def init_meltano(self):
        print(f"Initializing Meltano... ")
        run(['meltano', 'init', str(self.workspace)])
        print(f"Initialized Meltano.")

    def init_config(self, output):
        templates = Path(__file__).parent / 'templates'
        copy(templates / 'meltano.yml', self.workspace / 'meltano.yml')
        with open(templates / 'labcrawler.json.template') as file:
            config_template = file.read()
        if output:
            output_dir = Path(output).expanduser().absolute()
        else:
            output_dir = Path(user_documents_dir()) / APPNAME
        with open(self.config_path, 'w') as config_file:
            config_file.write(config_template.format(output_dir=output_dir))

    def init_plugins(self):
        chdir(self.workspace)
        print("Installing Meltano plugins...")
        run(['meltano', 'install'])
        print("Installed Meltano plugins")

    @property
    def config(self):
        """When reading the config file, only read it once"""
        if not hasattr(self, '_config'):
            with open(self.config_path) as config_file:
                self._config = load(config_file)
        return self._config

    @staticmethod
    def grab_token():
        if 'GITLAB_PRIVATE_TOKEN' not in environ:
            secret = getpass("GitLab Private Token: ").strip()
            if len(secret) != 26:
                raise RuntimeError(
                    "GitLab Private Token must contain 26 characters")
            environ['GITLAB_PRIVATE_TOKEN'] = secret

    def melt(self, namespace):
        """Load all the data via meltano"""
        if not self.workspace.exists():
            raise RuntimeError("Use the init command first")
        output_dir = self.config['output_dir']
        self.clear_dir("previous output", Path(output_dir))
        chdir(self.workspace)
        for source in SOURCES:  # FAKE: we only really support 1 source
            csv_dir = Path(output_dir) / source
            csv_dir.mkdir()
            self.grab_token()
            environ['OUTPUT_DIR'] = str(csv_dir)
            environ['GITLAB_API_URL'] = self.config['api_url']

            # HACK: Work with longer lists of groups - insert a list into the
            # YAML environ['GITLAB_GROUPS'] = ' '.join(self.config['groups'])
            groups = self.config['groups']
            with open('meltano.yml') as file:
                myaml = yaml.load(file, Loader=yaml.Loader)
            myaml['plugins']['extractors'][0]['config']['groups'] = groups
            with open('meltano.yml', 'w') as file:
                file.write(yaml.dump(myaml))

            run(['meltano', 'run', 'tap-gitlab', 'target-csv'])
        print(f"Output is in {output_dir}")

    def load(self, namespace):
        """Load CI includes (and later blames), not covered by meltano"""
        # Cheap and easy cli argument: give me PROJECT_ID to limit scope
        self.grab_token()
        if 'PROJECT_ID' in os.environ:
            loader = GitLabCIDataLoader(self.config,
                                        project_id=os.environ['PROJECT_ID'])
        else:
            loader = GitLabCIDataLoader(self.config)
        loader.load_files()
        loader.load_blames()

    def analyze(self, namespace):
        banner = "Globals: pandas, neat\n\n"
        values = {}
        values['neat'] = output_neat
        values['pandas'] = pandas
        for source in SOURCES:
            csv_dir = Path(self.config['output_dir']) / source
            analyzer = GitLabAnalyzer(csv_dir)
            banner += f"{source}\n"
            for datatype in analyzer.datatypes:
                if hasattr(analyzer, datatype):
                    num = len(getattr(analyzer, datatype).index)
                    banner += f"{num:>8} " + \
                        f"{datatype}\n"
            banner += "         raw\n"
            values[source] = analyzer
        banner = f"\nLabCrawler analysis\n{banner}\n" + \
            "Python {python_version()}" + \
            " ctrl-d to quit"
        pandas.set_option('display.max_rows', None)
        interact(local=values, banner=banner)
