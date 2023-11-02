from dataclasses import dataclass
import logging
from urllib.parse import quote
from requests import get


@dataclass
class GitLabRepositoryFilesExtractor:

    # 2 general attributes (typically from environment variables)

    gitlab_private_token: str
    gitlab_api_url: str

    @property
    def headers(self):
        return {'Private-Token': self.gitlab_private_token}

    def query_repository_files(self, query: str, project_id: int, branch: str,
                               repo_path: str):
        """Convenience method to perform a query"""
        id = str(project_id)
        root = self.gitlab_api_url
        path = quote(repo_path)
        url = f"{root}/api/v4/projects/{id}/repository/files/{path}/{query}"
        params = {'ref': quote(branch)}
        response = get(url, params=params, headers=self.headers)
        logging.info(f"{url}?ref={params['ref']} - {response.status_code}")
        return response

    def extract_blames(self, project_id: int, branch: str, repo_path: str):
        """Pull all the blame data for a file and return it"""
        response = self.query_repository_files('blame', project_id, branch,
                                               repo_path)
        if response.ok:
            return response.json()

    def extract_file_content(self, project_id: int, branch: str, repo_path: str):
        """Pull the content of a file and return it as text"""
        response = self.query_repository_files('raw', project_id, branch,
                                               repo_path)
        if response.ok:
            return response.text

    def extract_blamed_committers(self, project_id: int, branch: str, repo_path: str):
        """
        Pull the blame data for a file and return only the blamed committers

        Keyword arguments:
        project_id:int -- database id of the project to query
        branch:str -- name of the branch to inspect
        repo_path:str -- path to the file within the repo

        Return value:
        List of dicts with project_id, committer name, committer email
        """
        blames = self.extract_blames(project_id=project_id,
                                     branch=branch, repo_path=repo_path)
        commits = [b['commit'] for b in blames or []]
        committers = {(c['committer_name'], c['committer_email'])
                      for c in commits}
        return [{'project_id': project_id, 'committer_name': c[0],
                'committer_email': c[1]} for c in sorted(committers)]
