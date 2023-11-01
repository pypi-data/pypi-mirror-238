from typing import List

import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder
from bpkio_api.helpers.times import to_local_tz, to_relative_time
from bpkio_cli.click_mods.group_rest_resource import ApiResourceGroup
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.click_helpers import get_api_endpoint, retrieve_resource
from bpkio_cli.core.resource_trail import ResourceTrail
from bpkio_cli.utils.datetimes import parse_date_expression_as_utc
from bpkio_cli.writers.breadcrumbs import display_resource_info


def create_child_resource_group(
    name: str,
    resource_class: type,
    endpoint_path: List[str],
    aliases: List[str] = [],
    default_fields=["id", "name"],
    extra_commands=[],
):
    """Generates a group of CLI commands for CRUD-based sub-resources

    Args:
        name (str): The name of the command group
        endpoint_path (List[str]): List of the endpoint names that make the path of the
            corresponding api class (eg. ["sources", "virtual-channel", "slots"])
        aliases (List[str], optional): Aliases for the command name. Defaults to none.
        default_fields (list, optional): Base resource fields used for table displays.
            Defaults to ["id", "name", "type"].
        with_content_commands (bool | str): Defines whether the group contains commands
            for handling resource content (for sources and services)

    Returns:
        cloup.Group: The MultiCommand group with all its nested commands
    """
    sections = []
    
    resource_title = str.title(name.replace("-", " "))
    if len(endpoint_path) > 1:
        parent_resource_title = str.title(
            endpoint_path[-2].replace("-", " ").replace("_", " ")
        )
        resource_title = f"{parent_resource_title} {resource_title}"

    # === GROUP ===

    @cloup.group(
        name=name,
        help=f"Commands for managing {resource_title}s",
        aliases=aliases,
        cls=ApiResourceGroup,
        show_subcommand_aliases=True,
        resource_class=resource_class,
    )
    @cloup.argument(
        "id",
        metavar=f"<{name.replace('-', '_')}_id>",
        help=(
            f"The identifier of the {resource_title} to work with. "
            f"Leave empty for commands operating on a list of {resource_title}s."
        ),
    )
    @SessionRecorder.do_not_record
    def resource_group(id):
        if id:
            resource = retrieve_resource(id, endpoint_path=endpoint_path)
            display_resource_info(resource)

    # === CRUD Commands ===

    # --- LIST Command
    @cloup.command(help=f"List all {resource_title}s", aliases=["ls"])
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.option(
        "-s",
        "--start",
        type=tuple,
        cls=OptionEatAll,
        default=("1 hour ago",),
        help="Start time",
    )
    @click.option(
        "-e",
        "--end",
        type=tuple,
        cls=OptionEatAll,
        default=("in 1 hour",),
        help="End time",
    )
    @click.pass_obj
    def list(
        obj: AppContext,
        list_format,
        select_fields,
        sort_fields,
        ids_only,
        start,
        end,
        **kwargs,
    ):
        endpoint = get_api_endpoint(endpoint_path)

        start = parse_date_expression_as_utc(start)
        end = parse_date_expression_as_utc(end)

        click.secho(
            "Looking at a window of time between {} ({}) and {} ({})".format(
                to_local_tz(start),
                to_relative_time(start),
                to_local_tz(end),
                to_relative_time(end),
            ),
            fg="white",
            dim=True,
        )

        resources = endpoint.list(obj.resources.last(), from_time=start, to_time=end)

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            ids_only=ids_only,
        )

    # --- INFO Commmand
    @cloup.command(help=f"Get a specific {resource_title} by ID")
    @bic_options.output_formats
    @click.pass_obj
    def info(obj: AppContext, list_format):
        resource = retrieve_resource(endpoint_path=endpoint_path)

        obj.response_handler.treat_single_resource(resource, format=list_format)

    # --- GET Commmand
    @cloup.command(
        aliases=["retrieve", "json"],
        help=f"Get the JSON representation of a single {resource_title} "
        f"or list of {resource_title}s",
    )
    @click.pass_obj
    def get(obj: AppContext):
        try:
            resource = retrieve_resource(endpoint_path=endpoint_path)
            obj.response_handler.treat_single_resource(resource, format="json")
        except Exception:
            endpoint = get_api_endpoint(endpoint_path)
            resources = endpoint.list(obj.resources.last())

            obj.response_handler.treat_list_resources(resources, format="json")

    # --- SEARCH Command
    @cloup.command(
        help=f"Retrieve a list of all {resource_title}s "
        "that match given terms in all or selected fields"
    )
    @bic_options.search
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.pass_obj
    def search(
        obj: AppContext,
        single_term,
        search_terms,
        search_fields,
        list_format,
        select_fields,
        sort_fields,
        ids_only,
    ):
        search_def = bic_options.validate_search(
            single_term, search_terms, search_fields
        )

        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.search(obj.resources.last(), filters=search_def)

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            ids_only=ids_only,
        )

    # --- DELETE Commmand
    @cloup.command(aliases=["del"], help=f"Delete a specific {resource_title} by ID")
    @click.confirmation_option(prompt="Are you sure you want to delete this resource?")
    @click.pass_context
    def delete(ctx):
        resource_context: ResourceTrail = click.get_current_context().obj.resources
        id = resource_context.last()
        parent_id = resource_context.parent()

        endpoint = get_api_endpoint(endpoint_path)
        endpoint.delete(parent_id, id)

        click.secho(f"Resource {id} deleted", fg="green")

    # --- CLEAR Command
    @cloup.command(help=f"Delete all {resource_title}s")
    @click.confirmation_option(
        prompt=f"Are you sure you want to delete all {resource_title}s?"
    )
    @click.pass_obj
    def clear(obj: AppContext, **kwargs):
        endpoint = get_api_endpoint(endpoint_path)
        (deleted, failed) = endpoint.clear(obj.resources.last())

        click.secho(f"Deleted {deleted} {resource_title}s", fg="green")
        if failed:
            click.secho(f"Failed to delete {failed} {resource_title}s", fg="red")

    sections.append(
        cloup.Section(
            "CRUD commands", [get, info, list, search, delete, clear]
        )
    )

    # === EXTRA Commands
    # Go through extra commands and add them where relevant...

    sections.append(cloup.Section("Other commands", []))

    for new_command in extra_commands:
        inserted = False
        for section in sections:
            for k in section.commands.keys():
                if k == new_command.name:
                    # ... override an existing one ...
                    section.commands[k] = new_command
                    inserted = True
        if not inserted:
            # ... or add it to the last section
            if new_command.name in ["create", "update", "delete"]:
                for section in sections:
                    if section.title == "CRUD commands":
                        section.add_command(new_command)
                        break
            else:
                sections[-1].add_command(new_command)

    # === END OF GROUP ===
    for section in sections:
        resource_group.add_section(section)
        
    return resource_group
