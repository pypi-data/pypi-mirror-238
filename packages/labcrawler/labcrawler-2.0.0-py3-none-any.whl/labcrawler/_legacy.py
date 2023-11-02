# Code to extract project-level CI configuration data, including the content of
# CI config file(s) and blames thereof. Ideally, we'd do this inside Meltano.
# But for now, it's more direct.

from pathlib import Path
from csv import DictReader
from csv import DictWriter
from os import environ
from dataclasses import dataclass
import logging
import sys
from argparse import ArgumentParser
from pprint import pp

from labcrawler.gitlab_legacy.gitlab_ci_config import GitLabCIConfig
from labcrawler.gitlab_legacy.gitlab_repository_files_extractor import \
    GitLabRepositoryFilesExtractor
from labcrawler.gitlab_legacy.project_data_file import ProjectDataFile

if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = ArgumentParser(prog='labcrawler')
    parser.add_argument('--project', '-p', action='store', type=int)
    parser.add_argument('--output', choices=['file', 'term'], default='term')
    parser.add_argument('--query',
                        choices=['committers', 'content', 'includes'],
                        default=['committers', 'content'], nargs='+')
    values = parser.parse_args(sys.argv[1:])

    project_file = ProjectDataFile()

    if values.project:
        project_ids = [values.project]
    else:
        project_ids = [p['id'] for p in project_file.projects_data]

    extractor = GitLabRepositoryFilesExtractor(
        gitlab_private_token=environ['GITLAB_PRIVATE_TOKEN'],
        gitlab_api_url=environ['GITLAB_API_URL'])

    if ('content' in values.query) or ('includes' in values.query):

        contents = []
        includes = []
        for project_id in project_ids:
            project_data = project_file.get_project_data(project_id)
            ci_config_file_content = extractor.extract_file_content(
                project_id=project_data['id'],
                branch=project_data['default_branch'],
                repo_path=project_data['ci_config_path'] or '.gitlab-ci.yml')
            if ('content' in values.query):
                contents.append(ci_config_file_content)
            if ('includes' in values.query):
                config = GitLabCIConfig(ci_config_file_content)
                if config.locals:
                    for localfile in config.locals:
                        includes.append({'project_id': project_data['id'],
                                         'local_include': localfile})

        if values.output == 'term':
            for item in contents:
                print(item)
            for row in includes:
                print(row)
        elif values.output == 'file':
            path = Path('output/ci_config_includes.csv')
            with open(path, 'w') as outfile:
                fieldnames = ['project_id', 'local_include']
                writer = DictWriter(outfile, fieldnames)
                writer.writeheader()
                for row in includes:
                    writer.writerow(row)
                logging.info(f"Wrote local includes to {str(path.absolute())}")

    if 'committers' in values.query:

        committers = []
        for project_id in project_ids:
            project_data = project_file.get_project_data(project_id)
            project_committers = extractor.extract_blamed_committers(
                project_id=project_data['id'],
                branch=project_data['default_branch'],
                repo_path=project_data['ci_config_path'] or '.gitlab-ci.yml')
            committers.extend(project_committers)

        if values.output == 'term':
            pp(committers)
        elif values.output == 'file':
            path = Path('output/ci_config_committers.csv')
            with open(path, 'w') as outfile:
                fieldnames = ['project_id',
                              'committer_name', 'committer_email']
                writer = DictWriter(outfile, fieldnames)
                writer.writeheader()
                for committer in committers:
                    writer.writerow(committer)
                logging.info(f"Wrote CI content to {str(path.absolute())}")
