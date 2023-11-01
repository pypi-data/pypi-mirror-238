import json as j
import re
from typing import List
from urllib.parse import quote_plus

import bpkio_api.mappings as mappings
import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.helpers.handlers.dash import DASHHandler
from bpkio_api.helpers.handlers.hls import HLSHandler
from bpkio_api.helpers.recorder import SessionRecorder
from bpkio_api.models.Services import ServiceIn
from bpkio_cli.click_mods.group_rest_resource import ApiResourceGroup
from bpkio_cli.commands.live_monitor import monitor_hls
from bpkio_cli.commands.package import package_resources
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.click_helpers import (
    get_api_endpoint,
    get_content_handler,
    retrieve_resource,
)
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.utils.editor import edit_payload
from bpkio_cli.utils.profile_maker import make_transcoding_profile
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.content_display import display_content
from bpkio_cli.writers.players import StreamPlayer
from bpkio_cli.writers.tables import display_table
from bpkio_cli.writers.urls import pretty_url


def create_resource_group(
    name: str,
    resource_class: type,
    endpoint_path: List[str],
    title: str | None = None,
    aliases: List[str] = [],
    default_fields=["id", "name", "type"],
    with_content_commands: List[str] = [],
    extra_commands: List[cloup.Command] = [],
):
    """Generates a group of CLI commands for CRUD-based resources

    Args:
        name (str): The name of the command group
        aliases (List[str], optional): Aliases for the command name. Defaults to none.
        default_fields (list, optional): Base resource fields used for table displays.
            Defaults to ["id", "name", "type"].
        endpoint_path (List[str]): List of the endpoint names that make the path of the
            corresponding api class (eg. ["sources", "virtual-channel"])
        with_content_commands (bool | List[str]): Defines whether the group contains
            commands for handling resource content (for sources and services)
        extra_commands (list): List of additional commands to add

    Returns:
        cloup.Group: The MultiCommand group with all its nested commands
    """
    resource_title = title if title else str.title(name.replace("-", " "))
    if len(endpoint_path) > 1:
        parent_resource_title = re.sub("s$", "", endpoint_path[0])
        resource_title = f"{resource_title} {parent_resource_title}"

    sections = []

    # === HELPER functions ===
    # Moved to click_helpers

    # === GROUP ===

    @cloup.group(
        name=name,
        help=f"Manage {resource_title}s",
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
            f"Leave empty for commands operating on a list of {resource_title}s. "
            "You can use $ and @ notation to refer to previously selected resources."
        ),
    )
    @click.pass_context
    @SessionRecorder.do_not_record
    def resource_group(ctx, id):
        if id:
            resource = retrieve_resource(id, endpoint_path=endpoint_path)
            if ctx.invoked_subcommand != "get":
                display_resource_info(resource)

    # === CRUD Commands ===

    # --- LIST Command
    @cloup.command(help=f"List all {resource_title}s", aliases=["ls"])
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.pass_obj
    def list(obj: AppContext, list_format, select_fields, sort_fields, ids_only):
        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.list()

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            ids_only=ids_only,
        )

    # --- INFO Commmand
    @cloup.command(
        aliases=["content"],
        help=f"Get detailed information about a specific {resource_title} by ID",
    )
    @bic_options.url
    @click.option(
        "--content/--no-content",
        "with_content",
        is_flag=True,
        default=True,
        help="Add or hide summary information about the content of the resource",
    )
    @click.pass_context
    def info(
        ctx,
        sub: int,
        url: str,
        fqdn: str,
        query: List[str],
        user_agent: str,
        header: bool = True,
        with_content: bool = True,
    ):
        resource = retrieve_resource(endpoint_path=endpoint_path)

        ctx.obj.response_handler.treat_single_resource(resource)

        # then show the summary table (if there is one)
        if with_content:
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if handler:
                try:
                    display_content(
                        handler=handler,
                        max=1,
                        interval=0,
                        table=True,
                        header=header,
                    )
                except BroadpeakIoCliError as e:
                    pass

    # --- GET Commmand
    @cloup.command(
        aliases=["retrieve", "json"],
        help=f"Get the JSON representation of a single {resource_title} by ID",
    )
    @click.pass_obj
    def get(obj: AppContext):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        obj.response_handler.treat_single_resource(resource, format="json")

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
        sort_fields,
        list_format,
        select_fields,
        ids_only,
    ):
        search_def = bic_options.validate_search(
            single_term, search_terms, search_fields
        )

        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.search(filters=search_def)

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
        resource = retrieve_resource(endpoint_path=endpoint_path)

        endpoint = get_api_endpoint(endpoint_path)
        endpoint.delete(resource.id)

        # remove from cache
        ctx.obj.cache.remove(resource)

        click.secho(f"Resource {resource.id} deleted", fg="green")

    # --- UPDATE Command
    @cloup.command(aliases=["put", "edit"], help=f"Update a {resource_title}")
    @click.pass_context
    def update(ctx):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        resource_id = resource.id

        # remap to an input model
        resource = mappings.to_input_model(resource)

        updated_resource = edit_payload(resource)

        endpoint = get_api_endpoint(endpoint_path)
        # TODO - try to parse into the resource class (otherwise can only work with specific resource sub-types)
        endpoint.update(resource_id, updated_resource)

        click.secho(f"Resource {resource_id} updated", fg="green")

    # --- DUPLICATE Command
    @cloup.command(aliases=["copy"], help=f"Duplicate a {resource_title}")
    @click.option(
        "-e",
        "--edit",
        help="Edit the duplicated resource before saving it",
        is_flag=True,
        default=False,
    )
    @click.pass_obj
    def duplicate(obj: AppContext, edit):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        endpoint = obj.api.root_endpoint_for_resource(resource)

        resource.name = resource.name + " (copy)"

        # remap to an input model
        resource = mappings.to_input_model(resource)

        if edit:
            resource = edit_payload(resource)

        new_resource = endpoint.create(resource)

        obj.response_handler.treat_single_resource(new_resource, format="json")

    sections.append(
        cloup.Section(
            "CRUD commands", [get, info, list, search, delete, update, duplicate]
        )
    )

    # === SERVICE Commands ===
    service_section = cloup.Section("Service commands", [])

    if issubclass(resource_class, ServiceIn):
        # --- PAUSE Command
        @cloup.command(aliases=["disable"], help="Disable (pause) a service")
        @click.pass_obj
        def pause(obj: AppContext):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            if resource.state == "paused":
                click.secho(f"Service state is already paused", fg="red")
            else:
                endpoint = obj.api.root_endpoint_for_resource(resource)

                updated_resource = endpoint.pause(resource.id)
                click.secho("Service state: ", fg="yellow", nl=False)
                click.secho(updated_resource.state, fg="yellow", bold=True)

        @cloup.command(aliases=["enable"], help="Enable (unpause) a service")
        @click.pass_obj
        def unpause(obj: AppContext):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            if resource.state == "enabled":
                click.secho(f"Service state is already enabled", fg="red")
            else:
                endpoint = obj.api.root_endpoint_for_resource(resource)

                updated_resource = endpoint.unpause(resource.id)
                click.secho("Service state: ", fg="yellow", nl=False)
                click.secho(updated_resource.state, fg="yellow", bold=True)

        service_section.add_command(pause)
        service_section.add_command(unpause)

        sections.append(service_section)

    # === CONTENT Commands ===

    content_section = cloup.Section("Content commands", [])

    if any(x in with_content_commands for x in ["all", "url"]):
        # --- URL Command
        @cloup.command(help="Retrieve the full URL of the resource")
        @bic_options.url
        def url(
            sub: int,
            url: str,
            fqdn: str,
            query: List[str],
            user_agent: str,
            **kwargs,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            full_url = resource.make_full_url()
            click.echo(pretty_url(full_url))
            click.echo()
            click.secho("> " + full_url, fg="yellow", dim=True)

            click.secho("\nCalculating resolved URL: ")
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            if handler:
                click.echo(pretty_url(handler.url))
                click.echo()
                click.secho("> " + handler.url, fg="yellow", dim=True)

        content_section.add_command(url)

    if any(x in with_content_commands for x in ["all", "check"]):
        # --- CHECK Command
        @cloup.command(help=f"Check the validity of an existing {resource_title}")
        @bic_options.list()
        @bic_options.output_formats
        @click.pass_obj
        def check(obj: AppContext, select_fields, sort_fields, list_format, **kwargs):
            id = obj.resources.last()
            endpoint = get_api_endpoint(endpoint_path[0:1])
            results = endpoint.check_by_id(id)

            obj.response_handler.treat_list_resources(
                results,
                format=list_format,
                select_fields=select_fields,
                sort_fields=sort_fields,
            )

        content_section.add_command(check)

    if any(x in with_content_commands for x in ["all", "read"]):
        # --- READ Command
        @cloup.command(
            help=f"Load and display the content of a {resource_title}"
            ", optionally highlighted with relevant information"
        )
        @bic_options.read
        @bic_options.url
        @bic_options.table
        @click.pass_obj
        def read(
            obj: AppContext,
            sub: int,
            url: str,
            fqdn: str,
            query: List[str],
            user_agent: str,
            table: bool,
            raw: bool,
            top: int = 0,
            tail: int = 0,
            header: bool = True,
            pager: bool = False,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if handler:
                try:
                    display_content(
                        handler=handler,
                        max=1,
                        interval=0,
                        table=table,
                        raw=raw,
                        top=top,
                        tail=tail,
                        header=header,
                        pager=pager,
                    )
                except BroadpeakIoCliError as e:
                    pass

        content_section.add_command(read)

    if any(x in with_content_commands for x in ["all", "poll"]):
        # --- POLL Command
        @cloup.command(
            help=f"Similar to `read`, but regularly re-load the {resource_title}"
            "source's content"
        )
        @bic_options.poll
        @bic_options.read
        @bic_options.url
        @bic_options.table
        def poll(
            sub: int,
            url: str,
            fqdn: str,
            query: List[str],
            user_agent: str,
            max: int,
            interval: int,
            raw: bool,
            diff: bool,
            top: bool,
            tail: bool,
            clear: bool,
            table: bool,
            pager: bool,
            silent: bool,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)

            if not resource.is_live():
                raise BroadpeakIoCliError(
                    "Polling can only be done for Live resources (sources or services)"
                )

            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            if handler:
                display_content(
                    handler,
                    max=max,
                    interval=interval,
                    table=table,
                    raw=raw,
                    diff=diff,
                    top=top,
                    tail=tail,
                    clear=clear,
                    pager=pager,
                    silent=silent,
                )

        content_section.add_command(poll)

    if any(x in with_content_commands for x in ["all", "monitor"]):
        # --- MONITOR Command
        @cloup.command(help="Check a live stream for significant markers")
        @bic_options.url
        @bic_options.poll
        @click.pass_obj
        def monitor(
            obj: AppContext,
            fqdn: str,
            url: str,
            query: List[str],
            user_agent: str,
            sub: int,
            max: int,
            interval: int,
            silent: bool,
            **kwargs,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            if not resource.is_live():
                raise BroadpeakIoCliError(
                    "Monitoring can only be done for Live resources (sources or services)"
                )

            if isinstance(handler, DASHHandler):
                raise NotImplementedError(
                    "Monitoring of DASH streams not yet implemented in BIC"
                )

            if isinstance(handler, HLSHandler) and handler.has_children():
                handler = handler.get_child(1)
                monitor_hls(
                    handler=handler,
                    max=max,
                    interval=interval,
                    silent=silent,
                    name=resource.summary,
                )

        content_section.add_command(monitor)

    if any(x in with_content_commands for x in ["all", "play"]):
        # --- PLAY Command
        @cloup.command(
            help=f"Open the URL of the {resource_title} in a web player",
            aliases=["open"],
        )
        @bic_options.url
        @click.option(
            "-p",
            "--player",
            default="CONFIG",
            help="The template for a player URL",
            type=str,
            is_flag=False,
            flag_value="CHOICE",
        )
        @click.pass_obj
        def play(
            obj: AppContext,
            fqdn: str,
            url: str,
            query: List[str],
            user_agent: str,
            sub: int,
            player: str,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )
            if player == "CONFIG":
                player = obj.config.get("player")

            if player == "CHOICE":
                player = StreamPlayer.prompt_player()

            # pass a set of useful parameters for placeholder replacement
            # in the player template

            if hasattr(resource, "get_all_fields_and_properties"):
                params = resource.get_all_fields_and_properties()
            else:
                params = dict(params)

            params.update(url=quote_plus(handler.url))

            StreamPlayer().launch(template=player, **params)

        content_section.add_command(play)

    if any(x in with_content_commands for x in ["all", "profile"]):
        # --- PROFILE Command
        @cloup.command(help=f"Create a profile from the {resource_title}")
        @click.option(
            "--table/--no-table",
            "with_table",
            is_flag=True,
            default=False,
            help="Add or hide summary information about the content of the resource",
        )
        @click.option(
            "--save",
            is_flag=True,
            default=False,
            help="Save the profile to a file",
        )
        @bic_options.url
        @click.pass_obj
        def profile(
            obj: AppContext,
            fqdn: str,
            url: str,
            query: List[str],
            user_agent: str,
            sub: int,
            with_table: bool,
            save: bool,
        ):
            resource = retrieve_resource(endpoint_path=endpoint_path)
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
            )

            (profile, messages) = make_transcoding_profile(handler)

            if with_table:
                display_table(profile["transcoding"]["jobs"])
            else:
                obj.response_handler.treat_single_resource(profile, format="json")

            if save:
                filename = f"profile_{resource.id}.json"
                with open(filename, "w") as f:
                    j.dump(profile, f, indent=4)
                click.secho(f"Profile saved to {filename}", fg="green")

            if messages:
                for message in messages:
                    click.echo(CL.log(message.message, message.level))
                click.secho(
                    "Since errors or warnings have been raised, you may want to review the profile payload to ensure it is usable",
                    fg="yellow",
                )

        content_section.add_command(profile)

    sections.append(content_section)

    # === PACKAGE Commands

    # COMMAND: PACKAGE
    @cloup.command()
    @cloup.option("-o", "--output", type=click.File("w"), required=False, default=None)
    @click.pass_obj
    def package(obj: AppContext, output):
        """Package a service and all its dependencies into a reusable recipe

        Args:
            output (str): Filename of the JSON file to write the package into
        """
        resource = retrieve_resource(endpoint_path=endpoint_path)

        package_resources([resource], obj.api, output)

    sections.append(cloup.Section("Other commands", [package]))

    # === EXTRA Commands
    # Go through extra commands and add them where relevant...

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
