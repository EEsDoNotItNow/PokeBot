

import argparse

from ..Log import Log

class DiscordArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        Log().error(message)
        raise ValueError(message)
