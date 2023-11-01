import csv
import json as j
import re
from io import StringIO
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

import click
import tabulate
from bpkio_api.models import BaseResource
from bpkio_cli.core.resource_recorder import ResourceRecorder
from bpkio_cli.utils.arrays import pluck_and_cast_properties, sort_objects
from bpkio_cli.writers.json_formatter import JSONFormatter
from bpkio_cli.writers.tables import display_table
from pydantic import BaseModel

tabulate.PRESERVE_WHITESPACE = True


class ResponseHandler:
    def __init__(self, cache: Optional[ResourceRecorder] = None) -> None:
        self.cache = None
        if cache:
            self.cache = cache

    def treat_list_resources(
        self,
        resources: List,
        select_fields: Optional[List[str]] = None,
        sort_fields: Optional[List[str]] = [],
        format: Optional[str] = None,
        ids_only: Optional[bool] = False,
    ):
        if not len(resources):
            return

        # Extract the select_fields
        if select_fields:
            select_fields = " ".join(select_fields)  # type: ignore
            select_fields = re.findall(r"\w[\w\.]*", select_fields)  # type: ignore
        else:
            select_fields = []

        # Sort the list
        if sort_fields and len(sort_fields):
            sort_by = " ".join(sort_fields)  # type: ignore
            sort_by = re.findall(r"\w[\w\.\:]*", sort_by)  # type: ignore
            sort_by = {
                i.split(":")[0]: i.split(":")[1] if len(i.split(":")) > 1 else "asc"
                for i in sort_by
            }
            # add sort fields to fields list if not already present
            for f in sort_by.keys():
                if f not in select_fields:
                    select_fields.append(f)

            resources = sort_objects(resources, sort_by=sort_by)

        # Register the (transformed) list into cache
        if self.cache:
            self.cache.record(resources)

        if ids_only:
            for r in resources:
                print(r.id)
            return

        # Output the JSON representation
        if format == "json":
            if isinstance(resources[0], BaseModel):
                resources = [j.loads(r.json(exclude_none=True)) for r in resources]

            colored_json = JSONFormatter().format(resources)
            click.echo(colored_json)
            return

        # Extract the select_fields
        if select_fields:
            select_fields = " ".join(select_fields)  # type: ignore
            select_fields = re.findall(r"\w[\w\.]*", select_fields)  # type: ignore

        data = pluck_and_cast_properties(resources, select_fields)

        if format == "csv":
            export_csv(data)
            return

        # Else print it as a table
        display_table(data, format=format)

    def treat_single_resource(
        self,
        resource: object,
        format: Optional[str] = None,
    ):
        # Record the resource
        if self.cache and hasattr(resource, "id"):
            self.cache.record(resource)

        if format == "json" and isinstance(resource, BaseModel):
            data = j.loads(resource.json(exclude_none=False))
            colored_json = JSONFormatter().format(data)
            click.echo(colored_json)

            return resource

        elif not isinstance(resource, BaseResource):
            colored_json = JSONFormatter().format(resource)
            click.echo(colored_json)

            return resource

        else:
            rows = []

            # Identifier
            header = "{} {}".format(
                click.style(resource.__class__.__name__, fg="white", dim=True),
                click.style(resource.id, fg="white"),
            )
            rows.append(header)

            # Name and description
            title = []
            title.append(click.style(resource.name, fg="white", bold=True))
            if hasattr(resource, "description") and resource.description is not None:
                title.append(click.style(resource.description, fg="white"))
            rows.append("\n".join(title))

            # URL
            if hasattr(resource, "url"):
                url = (
                    resource.make_full_url()
                    if hasattr(resource, "make_full_url")
                    else resource.url
                )
                base_url = click.style(url.split("?")[0], fg="yellow")
                if hasattr(resource, "assetSample"):
                    base_url = base_url.replace(resource.assetSample, "") + click.style(
                        resource.assetSample, fg="yellow", dim=True
                    )

                lines = [base_url]
                parsed = urlparse(url)
                qs = parse_qs(parsed.query, keep_blank_values=0, strict_parsing=0)
                for i, (k, v) in enumerate(qs.items()):
                    separator = "?" if i == 0 else "&"
                    elements = [
                        " " + separator,
                        click.style(k, fg="yellow"),
                        "=",
                        click.style(v[0], fg="green"),
                    ]
                    lines.append(" ".join(elements))
                rows.append("\n".join(lines))

            display_table(rows, format=format)

    @staticmethod
    def treat_simple_list(data: list):
        click.echo(tabulate.tabulate(data, headers="keys"))
        return


def export_csv(data):
    # Find all unique keys
    keys = list()
    for obj in data:
        for k in obj.keys():
            if k not in keys:
                keys.append(k)

    # Write to CSV
    output = StringIO()
    dict_writer = csv.DictWriter(output, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

    # Get CSV data as a string
    csv_str = output.getvalue()
    print(csv_str)

    # Close the StringIO object
    output.close()
