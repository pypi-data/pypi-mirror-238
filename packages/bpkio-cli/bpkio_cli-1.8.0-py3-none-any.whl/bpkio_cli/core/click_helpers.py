import click
from bpkio_api.models import ServiceIn, SourceIn
from bpkio_cli.core.resource_trail import ResourceTrail
from bpkio_cli.utils.url_builders import get_service_handler, get_source_handler


def retrieve_resource(
    id: int | str | None = None,
    endpoint_path: list = [],
):
    ctx = click.get_current_context()
    resource_context: ResourceTrail = ctx.obj.resources
    if not id:
        id = resource_context.last()
    endpoint = get_api_endpoint(endpoint_path)

    parent_id = resource_context.parent()
    if parent_id:
        resource = endpoint.retrieve(parent_id, id)
    else:
        resource = endpoint.retrieve(id)

        # Record the resource
        if ctx.obj.cache and hasattr(resource, "id"):
            ctx.obj.cache.record(resource)

    return resource


def get_api_endpoint(path: list):
    api = click.get_current_context().obj.api
    endpoint = api
    for p in path:
        endpoint = getattr(endpoint, p)
    return endpoint


def get_content_handler(
    resource,
    replacement_fqdn=None,
    extra_url=None,
    additional_query_params=[],
    subplaylist_index=None,
    user_agent=None,
):
    api = click.get_current_context().obj.api

    if isinstance(resource, SourceIn):
        return get_source_handler(
            resource,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            subplaylist_index=subplaylist_index,
            user_agent=user_agent,
        )

    if isinstance(resource, ServiceIn):
        return get_service_handler(
            resource,
            replacement_fqdn=replacement_fqdn,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            subplaylist_index=subplaylist_index,
            api=api,
            user_agent=user_agent,
        )
