import click
import cloup
from bpkio_api.helpers.times import relative_time
from bpkio_api.models import (
    VirtualChannelService,
    VirtualChannelSlotIn,
    VirtualChannelSlotType,
)
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.utils.datetimes import (
    parse_date_expression_as_utc,
    parse_duration_expression,
)


def create_slot_command():
    # COMMAND: CREATE VC SLOT
    @cloup.command(help="Quickly add a slot")
    @click.option(
        "--type",
        "slot_type",
        default="AD_BREAK",
        help="Type of slot",
        type=click.Choice(VirtualChannelSlotType._member_names_, case_sensitive=False),
    )
    @click.option(
        "--in",
        "slot_start",
        type=tuple,
        cls=OptionEatAll,
        default="30 sec",
        help="When the slot will start",
    )
    @click.option(
        "--for",
        "slot_duration",
        type=tuple,
        cls=OptionEatAll,
        default="1 min",
        help="Duration of the slot",
    )
    @click.pass_obj
    def create(obj: AppContext, slot_type, slot_start, slot_duration):
        vc_id = obj.resources.last()
        create_vc_slot(obj, vc_id, slot_type, slot_start, slot_duration)

    return create


def create_vc_slot(context: AppContext, vc_id, slot_type, break_start, break_duration):
    api = context.api.services.virtual_channel
    vc: VirtualChannelService = api.retrieve(vc_id)

    start_time = parse_date_expression_as_utc(break_start, future=True)
    duration = parse_duration_expression(break_duration)

    if slot_type == VirtualChannelSlotType.AD_BREAK.name:
        slot = VirtualChannelSlotIn(
            name="Ad Break (from bic)",
            startTime=start_time,
            duration=duration,
            type=VirtualChannelSlotType.AD_BREAK,
        )
        slot = api.slots.create(vc.id, slot)
    elif slot_type == VirtualChannelSlotType.CONTENT.name:
        raise NotImplementedError("Content slots are not yet supported")
    else:
        raise BroadpeakIoCliError(f"Unknown slot type {slot_type}")

    context.response_handler.treat_single_resource(slot, format="json")
