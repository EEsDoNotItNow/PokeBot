

import argparse

from ..Log import Log



class DiscordArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):

            from contextlib import redirect_stdout
            import io
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    return super().parse_args(*args, **kwargs)
            except SystemExit:
                return f.getvalue()



    def error(self, message):
        Log().error(message)
        raise ValueError(message)
