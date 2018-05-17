
from contextlib import redirect_stdout
import argparse
import io

from ..Log import Log



class DiscordArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    return super().parse_args(*args, **kwargs)
            except SystemExit:
                Log().info("Sys Exit Capture")
                return f.getvalue()


    def error(self, message):
        raise ValueError(message)
