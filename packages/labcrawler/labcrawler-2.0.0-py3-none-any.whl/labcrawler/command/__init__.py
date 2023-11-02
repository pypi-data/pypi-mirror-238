from dataclasses import dataclass

from wizlib.command_handler import Command
from wizlib.config_machine import ConfigMachine


@dataclass
class LabCrawlerCommand(ConfigMachine, Command):

    appname = 'labcrawler'
    default = 'list'
    gitlab_host: str = ''

    @classmethod
    def add_app_args(self, parser):
        parser.add_argument('--gitlab-host')
