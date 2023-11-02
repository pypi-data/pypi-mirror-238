from dataclasses import dataclass
from argparse import ArgumentParser
import os
from getpass import getpass

from labcrawler.command import LabCrawlerCommand
from labcrawler.gitlab.query import GitLabQuery


@dataclass
class ListCommand(LabCrawlerCommand):

    datatype: str = ''
    path: str = ''
    name = 'list'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('datatype', choices=['groups', 'projects'])
        parser.add_argument('path')

    @LabCrawlerCommand.wrap
    def execute(self):
        host = self.config_get('gitlab-host')
        token = self.config_get('gitlab-token')
        if not host:
            raise RuntimeError("Missing host for GitLab API call")
        elif not token:
            token = getpass(f"GitLab Private Token for {host}: ").strip()
        if len(token) != 26:
            raise RuntimeError(
                "GitLab Access Token must contain 26 characters")
        cls = GitLabQuery.family_member('name', self.datatype)
        query = cls(host, token)
        result = query.run(self.path)
        self.status = f"{len(result)} {self.datatype} listed"
        return "\n".join([i['fullPath'] for i in result])
