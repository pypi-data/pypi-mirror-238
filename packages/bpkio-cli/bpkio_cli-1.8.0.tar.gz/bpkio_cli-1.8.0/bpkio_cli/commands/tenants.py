import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.models import Tenant
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.core.app_context import AppContext


def add_tenants_commands():
    return create_resource_group(
        "tenant",
        resource_class=Tenant,
        endpoint_path=["tenants"],
        aliases=["tnt", "tenants"],
        default_fields=["id", "name", "email", "state"],
        extra_commands=[reset_quotas],
    )


# COMMAND: RESET-QUOTAS
@cloup.command(help="Reset the tenant quotas")
@click.confirmation_option(prompt="Are you sure that you have the correct tenant?")
@click.pass_obj
def reset_quotas(obj: AppContext, **kwargs):
    id = obj.resources.last()

    obj.api.tenants.reset_quotas(tenant_id=id)
    # If an error is raised, the code will stop before the next line
    click.secho(f"Quotas reset for tenant {id}", fg="green")
