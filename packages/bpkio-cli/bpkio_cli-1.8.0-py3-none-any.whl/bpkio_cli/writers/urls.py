from typing import Optional
from urllib.parse import parse_qs, urlparse

import click


def pretty_url(
    url, path_highlight: Optional[str] = None, highlight_placeholder_params=True
):
    parsed = urlparse(url)
    base_url = click.style(f"{parsed.scheme}://{parsed.netloc}", fg="magenta")
    lines = [base_url]

    path = click.style("  " + parsed.path, fg="yellow")
    if path_highlight:
        path = path.replace(path_highlight, "") + click.style(
            path_highlight, fg="yellow", dim=True
        )
    lines.append(path)

    qs = parse_qs(parsed.query, keep_blank_values=False, strict_parsing=False)
    for i, (k, v) in enumerate(qs.items()):
        style = dict(fg="blue", bold=True)
        if highlight_placeholder_params:
            if v[0].startswith("$arg_"):
                style["fg"] = "green"
                style["bold"] = False
            elif v[0].startswith("$"):
                style["fg"] = "red"
                style["bold"] = False

        separator = "?" if i == 0 else "&"
        elements = [
            "    " + click.style(separator, fg="white", dim=True),
            click.style(k, fg="cyan"),
            click.style("=", fg="white", dim=True),
            click.style(v[0], **style),
        ]
        lines.append(" ".join(elements))

    return "\n".join(lines)
