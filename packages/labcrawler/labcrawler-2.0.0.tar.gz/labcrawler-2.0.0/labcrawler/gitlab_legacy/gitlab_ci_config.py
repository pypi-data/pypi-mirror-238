import re
from dataclasses import dataclass

import yaml


URL_PATTERN = re.compile(r'^\w+\:\/\/')


@dataclass
class GitLabCIConfig:
    """Parse GitLab CI config YAML text to discern useful info"""

    text: str

    @property
    def yaml(self):
        """Parse the yaml"""
        if self.text:
            return yaml.load(self.text, Loader=yaml.Loader)

    @staticmethod
    def local(element):
        """If the yaml element is 'local' then return the string"""
        if isinstance(element, str):
            if not URL_PATTERN.match(element):
                return element
        if isinstance(element, dict) and 'local' in element:
            return element['local']

    @property
    def locals(self):
        """Return the local includes"""
        if self.yaml and 'include' in self.yaml:
            element = self.yaml['include']
            if isinstance(element, str):
                if not URL_PATTERN.match(element):
                    return {element}
            if isinstance(element, list):
                return {self.local(i) for i in element if self.local(i)}
