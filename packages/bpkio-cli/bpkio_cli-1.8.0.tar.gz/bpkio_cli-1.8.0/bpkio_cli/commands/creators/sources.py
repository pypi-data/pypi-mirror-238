import re
from urllib.parse import urlparse, urlunparse

import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.helpers.source_type import SourceTypeDetector
from bpkio_api.models import (
    AdServerSourceIn,
    AssetCatalogSourceIn,
    AssetSourceIn,
    LiveSourceIn,
    SlateSourceIn,
    SourceType,
)
from bpkio_cli.core.app_context import AppContext
from InquirerPy.base.control import Choice


@cloup.command(
    help="Create a Source from just a URL. "
    "The CLI will work out what type of Source it is and create it accordingly"
)
@cloup.argument("url", help="URL of the source", required=False)
@cloup.option("--name", help="Name for the source", required=False)
@cloup.option(
    "--assist/--no-assist", help="Assist with the creation of the source", default=True
)
@click.pass_obj
def create(obj: AppContext, url: str, name: str, assist: bool):
    metadata_cache = obj.cache

    if not url:
        url = prompt.text(
            message="URL of the source",
            validate=lambda url: re.match(r"^https?://", url.strip()),
            invalid_message=("Your URL must be a valid HTTP URL"),
        )

    source_type = SourceTypeDetector.determine_source_type(url)
    if not source_type:
        raise Exception("Could not determine the type of source for that URL")

    click.secho("This appears to be a source of type: %s" % source_type.value)

    if source_type == SourceType.ASSET:
        source_type = prompt.select(
            message="From this, create",
            choices=[
                Choice(SourceType.ASSET, name="Asset"),
                Choice(SourceType.ASSET_CATALOG, name="Asset Catalog"),
            ],
            multiselect=False,
        )

    if source_type == SourceType.ASSET_CATALOG:
        url_parts = urlparse(url)
        path_parts = url_parts.path.split("/")[1:-1]
        paths = ["/"]
        last_path = ""
        for p in path_parts:
            last_path = last_path + "/" + p
            paths.append(last_path + "/")

        common_path = prompt.select(
            message="Common path for all assets",
            choices=paths,
            multiselect=False,
        )

        new_url = url_parts._replace(path=common_path, query="")
        new_url = urlunparse(new_url)

        sample = url.replace(new_url, "")

    if not name:
        name = prompt.text(message="Name for the source")

    match source_type:
        case SourceType.LIVE:
            source = obj.api.sources.live.create(LiveSourceIn(name=name, url=url))
        case SourceType.AD_SERVER:
            (url, queries, metadata) = treat_adserver_url(url, assist=assist)
            source = obj.api.sources.ad_server.create(
                AdServerSourceIn(name=name, url=url, queries=queries)
            )
            for k, v in metadata.items():
                metadata_cache.record_metadata(source, k, v)

        case SourceType.SLATE:
            source = obj.api.sources.slate.create(SlateSourceIn(name=name, url=url))
        case SourceType.ASSET:
            source = obj.api.sources.asset.create(AssetSourceIn(name=name, url=url))
        case SourceType.ASSET_CATALOG:
            source = obj.api.sources.asset_catalog.create(
                AssetCatalogSourceIn(name=name, url=new_url, assetSample=sample)
            )
        case _:
            raise click.BadArgumentUsage("Unrecognised source type '%s'" % source_type)

    obj.response_handler.treat_single_resource(source)


def treat_adserver_url(url, assist: bool = True):
    metadata_to_save = {}

    SYSTEM_VALUES = [
        ("$MMVAR_CACHE_BUSTER", "Cachebuster value"),
        ("$MAP_REMOTE_ADDR", "Client IP address (from header 'X-Forwarded-For')"),
        (
            "$_MMVAR_LIVEAR_SIGNALID",
            "Signal ID (from the SCTE35 marker)",
        ),
        (
            "$_MMVAR_LIVEAR_UPID",
            "UPID (from the SCTE35 marker)",
        ),
        ("$_MMVAR_LIVEAR_SLOTDURATION", "Slot duration (in seconds)"),
        (
            "${_MMVAR_LIVEAR_SLOTDURATION}000",
            "Slot duration (in microseconds)",
        ),
    ]

    parts = url.split("?")

    if len(parts) == 1:
        parts.append("")

    queries = parts[1]

    if len(queries) and assist:
        updated_queries = []
        for p in queries.split("&"):
            (k, val) = p.split("=")
            original_val = val

            # Suggest replacement for query parameters
            treatment = prompt.fuzzy(
                message=f"Parameter '{k}' (current value '{val}')",
                choices=[
                    Choice("keep", name="keep unchanged"),
                    Choice("static", name="STATIC: a static value"),
                    Choice(
                        "arg",
                        name="PARAM: pass-through from a query parameter on service URL (as $arg_*)",
                    ),
                    Choice(
                        "header",
                        name="HEADER: pass-through from a header on service URL (as $http_*)",
                    ),
                    Choice("system", name="SYSTEM: pass-through of a system value"),
                    Choice("remove", name="Remove this parameter"),
                ],
            )

            if treatment == "keep":
                val = val

            if treatment == "static":
                val = prompt.text(message="Value", default=val, level=1)

            if treatment == "arg":
                if val.startswith("$arg_"):
                    val = val.replace("$arg_", "")
                # if val.startswith(("{", "[")):
                #     val = re.sub(r"[\{\}\[\]]", "", val).lower()
                else:
                    val = k

                val = prompt.text(
                    message="Name of the incoming parameter",
                    default=val,
                    transformer=lambda s: make_dynamic_param(s, "param"),
                    level=1,
                )

                metadata_to_save[val] = original_val
                val = make_dynamic_param(val, "param")

            if treatment == "header":
                val = prompt.fuzzy(
                    message="Incoming header",
                    choices=["User-Agent", "Host", "X-Forwarded-For", "(other)"],
                    filter=lambda s: make_dynamic_param(s, "header")
                    if s != "(other)"
                    else s,
                    transformer=lambda s: make_dynamic_param(s, "header")
                    if s != "(other)"
                    else s,
                    level=1,
                )

                if val == "(other)":
                    val = prompt.text(
                        message="Name of the incoming header",
                        filter=lambda s: make_dynamic_param(s, "header"),
                        transformer=lambda s: make_dynamic_param(s, "header"),
                        level=1,
                    )

            if treatment == "system":
                val = prompt.fuzzy(
                    message="System value:",
                    choices=[
                        Choice(s[0], name=f"{s[0]}: {s[1]}") for s in SYSTEM_VALUES
                    ],
                    level=1,
                )

            if treatment == "remove":
                continue

            updated_queries.append(k + "=" + val)

        queries = "&".join(updated_queries)

    return (parts[0], queries, metadata_to_save)


def make_dynamic_param(name, mode):
    if mode == "header":
        return f"$http_{name.lower().replace('-','_')}"
    if mode == "param":
        return f"$arg_{name.lower().replace('-','_')}"
