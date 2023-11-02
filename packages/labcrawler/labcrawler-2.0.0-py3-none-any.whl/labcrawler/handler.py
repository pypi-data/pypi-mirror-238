import sys

# Specific to logging
import logging

from wizlib.command_handler import CommandHandler
from labcrawler.command import LabCrawlerCommand


class LabCrawlerHandler(CommandHandler):

    @classmethod
    def shell(cls):

        # TODO: Move logging setup to wizlib

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        super().shell(LabCrawlerCommand)
