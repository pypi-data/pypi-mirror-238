from pathlib import Path
from dataclasses import dataclass
from sys import argv
from inspect import get_annotations

from pandas import DataFrame
from pandas import read_csv
from tabulate import tabulate

from labcrawler.analyzers import Abstract


class GitLabAnalyzer:

    source = 'gitlab'

    datatypes = [
        'access_levels',
        'groups',
        'projects',
        'branches',
        'merge_requests',
        'project_members',
        'group_members',
        'users',
        'ci_config_committers',
        'ci_config_paths']

    def load_raw_from_csv(self, output_path_str: str):
        output_path = Path(output_path_str).expanduser()
        self.raw = Abstract()
        for datatype in self.datatypes:
            path = output_path / f'{datatype}.csv'
            if path.exists():
                with open(path) as dtfile:
                    dtframe = read_csv(dtfile)
                    setattr(self.raw, datatype, dtframe)

    def __init__(self, output_path_str: str):
        self.load_raw_from_csv(output_path_str)
        self.access_levels = \
            DataFrame(data=[[0, 'No access'], [5, 'Minimal access'],
                            [10, 'Guest'], [20, 'Reporter'], [
                30, 'Developer'], [40, 'Maintainer'],
                [50, 'Owner']], columns=['id', 'name']).set_index('id')
        if hasattr(self.raw, 'groups'):
            self.groups = self.raw.groups.set_index('id')
        if hasattr(self.raw, 'projects'):
            self.projects = self.raw.projects.set_index('id')
        if hasattr(self.raw, 'users'):
            self.users = self.raw.users.set_index('id')
        if hasattr(self.raw, 'branches'):
            self.branches = self.raw.branches.set_index('project_id').\
                join(self.projects[['name', 'path_with_namespace']].add_prefix(
                    'project_'))
        if hasattr(self.raw, 'merge_requests'):
            self.merge_requests = self.raw.merge_requests.set_index('project_id').\
                join(self.projects[['name', 'path_with_namespace']].add_prefix(
                    'project_'))
        if hasattr(self.raw, 'project_members'):
            self.project_members = self.raw.project_members.\
                join(self.projects[['name', 'path_with_namespace']].add_prefix('project_'), on='project_id').\
                join(self.users[['username']].add_prefix('user_'), on='user_id').\
                join(self.access_levels[['name']].add_prefix(
                    'access_level_'), on='access_level')
        if hasattr(self.raw, 'group_members'):
            self.group_members = self.raw.group_members.\
                join(self.groups[['path']].add_prefix('group_'), on='group_id').\
                join(self.access_levels[['name']].add_prefix(
                    'access_level_'), on='access_level')
        if hasattr(self.raw, 'ci_config_committers'):
            self.ci_config_committers = self.raw.ci_config_committers.\
                join(self.projects[['name', 'path_with_namespace']].add_prefix(
                    'project_'), on='project_id')
        if hasattr(self.raw, 'ci_config_paths'):
            self.ci_config_paths = self.raw.ci_config_paths.\
                join(self.projects[['name', 'path_with_namespace']].add_prefix(
                    'project_'), on='project_id', how='right')

        for datatype in self.datatypes:
            if hasattr(self, datatype):
                df = getattr(self, datatype)
                df.index.name = 'id'


def output_neat(dataframe):
    print(tabulate(dataframe, showindex=False, headers=dataframe.columns))
