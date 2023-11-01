import functools

from cloup import option, option_group


# Common parameters for READ and POLL
def poll_options(fn):
    @option_group(
        "Polling options",
        option(
            "--max",
            type=int,
            is_flag=False,
            default=-2,
            help="Number of times to poll before stopping. Don't specify or set to 0 for infinite polling",
        ),
        option(
            "-i",
            "--interval",
            type=int,
            default=4,
            help="Polling frequency to re-read the source's content",
        ),
        option(
            "-d",
            "--diff",
            is_flag=True,
            type=bool,
            default=False,
            help="Highlight the difference with last polled data (requires `--poll`)",
        ),
        option(
            "--clear/--no-clear",
            is_flag=True,
            default=True,
            help="Clear the screen first when polling",
        ),
        option(
            "--silent",
            help="Turn off audible alerts",
            is_flag=True,
            default=False,
        ),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
