from typing import Callable, Optional
from urllib.parse import parse_qs, urlparse

import click


class Colorizer:
    @staticmethod
    def node(text):
        return click.style(text, fg="white", bold=True)

    @staticmethod
    def attr(text):
        return click.style(text, fg="bright_blue")

    @staticmethod
    def value(text):
        return click.style(text, fg="cyan")

    @staticmethod
    def markup(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def past(text):
        return click.style(text, fg="white", dim=True)

    @staticmethod
    def future(text):
        return click.style(text, fg="green", dim=False)

    @staticmethod
    def high1(text):
        return click.style(text, fg="yellow")

    @staticmethod
    def high2(text):
        return click.style(text, fg="yellow", bold=True)

    @staticmethod
    def high3(text):
        return click.style(text, fg="magenta", bold=True)

    @staticmethod
    def url(text):
        return Colorizer.split_url(text, fg="yellow", italic=True)

    @staticmethod
    def url2(text):
        return Colorizer.split_url(text, fg="green", italic=True)

    @staticmethod
    def expand(text):
        return click.style(text, fg="bright_black", italic=True)

    @staticmethod
    def error(text):
        return click.style(text, fg="red", italic=False)

    @staticmethod
    def alert(text):
        return click.style(text, fg="red", bold=True)

    @staticmethod
    def alert_rev(text):
        return click.style(text, fg="red", reverse=True)

    @staticmethod
    def label(text):
        return click.style(text, fg="black", bg="black", bold=True)

    @staticmethod
    def make_separator(
        text: Optional[str] = None, length: Optional[int] = None, mode=None
    ):
        # if text:
        #     dashes = "-" * len(text)
        # else:
        #     if not length:
        length = 50
        dashes = "-" * length

        if mode == "xml":
            dashes = f"<!-- {dashes} -->"
        if mode == "hls":
            dashes = f"## {dashes}"

        return Colorizer.high3(dashes)

    @staticmethod
    def log(text, type):
        match str(type).lower():
            case "warning":
                return Colorizer.high1(f"[Warning] {text}")
            case "info":
                return Colorizer.attr(text)
            case "error":
                return Colorizer.error(f"[Error] {text}")

    @staticmethod
    def labeled(
        text,
        label,
        value_style: Optional[Callable] = None,
        label_style: Optional[Callable] = None,
    ):
        if label_style:
            lbl = label_style(label)
        else:
            lbl = Colorizer.label(label)

        if value_style:
            return f"{lbl} {value_style(text)}"
        else:
            return f"{lbl} {text}"

    @staticmethod
    def split_url(url, fg, italic=True):
        strings = []
        parsed = urlparse(url)

        if parsed.scheme:
            strings.append(click.style(parsed.scheme + "://", fg=fg, bold=True))
        if parsed.netloc:
            strings.append(
                click.style(
                    parsed.netloc,
                    fg=fg,
                    bold=True,
                )
            )

        path_parts = parsed.path.split("/")
        last_path_part = path_parts.pop(-1)
        if len(path_parts) > 0:
            strings.append(
                click.style("/".join(path_parts) + "/", fg=fg, italic=italic)
            )
        strings.append(
            click.style(
                last_path_part,
                fg=fg,
                reverse=True,
                bold=True,
                italic=italic,
            )
        )

        qs = parse_qs(parsed.query, keep_blank_values=0, strict_parsing=0)
        for i, (k, v) in enumerate(qs.items()):
            separator = "?" if i == 0 else "&"
            strings.append(
                click.style(separator + k + "=", fg=fg, italic=italic, bold=True)
            )
            strings.append(click.style(f"{v[0]}", fg=fg, italic=italic, dim=True))

        if parsed.fragment:
            strings.append(
                click.style("#" + parsed.fragment, fg=fg, italic=italic, dim=True)
            )

        # Add query params
        return "".join(strings)
