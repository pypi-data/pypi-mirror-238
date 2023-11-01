import functools

import click
from bpkio_cli.utils.urls import validate_ipv4_or_domain
from cloup import option, option_group


# Common parameters for READ and POLL
def url_options(fn):
    @option_group(
        "Content fetching options",
        option(
            "-s",
            "--sub",
            type=int,
            default=None,
            is_flag=False,
            flag_value="1",
            help="For formats that contain links to child / related payloads, "
            + "read a child instead (by index - as listed by the `read --table` command) "
            + "Leave empty defaults to the first one. "
            + "This option is primarily for use with HLS and VMAP formats.",
        ),
        option(
            "-u",
            "--url",
            type=str,
            default=None,
            help="Full URL of URL sub-path (for asset catalogs) to fetch",
        ),
        option(
            "-f",
            "--fqdn",
            type=str,
            default=None,
            is_flag=False,
            flag_value="SELECT",
            help="FQDN to use instead of the resource's own. "
            + "This option only applies to Services, and is typically "
            + "used to redirect the call through a CDN",
            callback=validate_fqdn,
        ),
        option(
            "-ua",
            "--user-agent",
            type=str,
            default=None,
            is_flag=False,
            flag_value="SELECT",
            help="Choose a different user agent to use when requesting the content. "
            + "Defaults to a standard Mozilla user agent if not set. "
            + "The value for the option is the label of a user-agent in the cli.cfg file, "
            + "the user-agent string itself, or leave empty to be presented with a choice.",
        ),
        option(
            "-q",
            "--query",
            type=str,
            multiple=True,
            help="Query parameters to add to the request. "
        )
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def validate_fqdn(ctx, param, value):
    # remove any protocol prefix is there is one
    if value and value != "SELECT":
        domain = value.split('://', 1)[-1]

        valid = validate_ipv4_or_domain(domain)
        if not valid:
            raise click.BadParameter("FQDN must be a valid IPv4 or domain name")
    return value
