import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import List, Optional, Tuple

import bpkio_cli.utils.sounds as sounds
import click
import m3u8
import progressbar
from bpkio_api.helpers.handlers.hls import HLSHandler
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.scte35 import summarize


class SignalType(Enum):
    PERIOD = "dash-period"
    DISCONTINUITY = "discontinuity"
    SCTE35_MARKER = "scte35-marker"
    DATERANGE = "daterange"
    HLS_MARKER = "hls-marker"
    DASH_EVENT = "dash-event"


class EventType(Enum):
    CUE_IN = "cue-in"
    CUE_OUT = "cue-out"
    AD = "ad"


@dataclass
class LiveSignal:
    type: SignalType
    appeared_at: datetime
    content: object
    payload: object | None = None
    disappeared_at: datetime | None = None
    num_appearances: int = 0
    event_type: EventType | None = None
    signal_time: datetime | None = None  # The time that the signal applies to, eg. PDT

    @property
    def id(self):
        if isinstance(self.content, m3u8.Segment):
            return (self.content.uri, self.content.current_program_date_time)


class LiveMonitor:
    def __init__(self) -> None:
        self.signals: dict = {}
        self.changes: dict = {}
        self._timestamp: datetime

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.end()
        else:
            self.end()

    def __repr__(self):
        return f"<LiveMonitor signals={len(self.signals)} [A:{len(self.changes['added'])} U:{len(self.changes['updated'])} R:{len(self.changes['removed'])}]>"

    def _reset(self):
        self.changes = dict(
            added=[],
            updated=[],
            removed=[],
        )

    def start(self, timestamp: Optional[datetime] = None):
        # Start a new "transaction"
        self._reset()
        self._timestamp = timestamp or datetime.now()

    def end(self):
        # End the "transaction"

        # Search for removed signals
        signal: LiveSignal
        for sid, signal in self.signals.items():
            if not signal.disappeared_at:
                if (
                    signal not in self.changes["updated"]
                    and signal not in self.changes["added"]
                ):
                    self.changes["removed"].append(signal)
                    self.signals[signal.id].disappeared_at = self._timestamp

    def record_signal(self, signal: LiveSignal) -> LiveSignal:
        # previously seen signal
        if signal.id in self.signals:
            signal = self.signals[signal.id]
            self.changes["updated"].append(signal)

        # new signal
        else:
            signal.appeared_at = self._timestamp
            self.changes["added"].append(signal)

        # then increment count and overwrite
        signal.num_appearances += 1
        self.signals[signal.id] = signal

        return signal


def monitor_hls(
    handler: HLSHandler,
    max: int,
    interval: int,
    silent: bool,
    name: Optional[str] = None,
):
    # Go through the HLS document and retrieve segments with specific markers

    click.secho("Limitations:", fg="yellow")
    click.secho(
        "- this feature only monitors the first rendition in the multi-variant playlist",
        fg="yellow",
    )
    click.secho("- this feature will only work with specific SCTE markers", fg="yellow")
    print()

    bar = progressbar.ProgressBar(
        widgets=[
            CL.high1("---[ "),
            CL.node(name),
            CL.high1(" ]--[ "),
            progressbar.RotatingMarker(),
            CL.high1(" ]--[ "),
            progressbar.Counter(),
            CL.high1(" @ "),
            progressbar.Variable(name="time", format="{formatted_value}"),
            CL.high1(" ]--[ "),
            "HLS media sequence: ",
            progressbar.Variable(name="sequence", format="{value}"),
            CL.high1(" ]---"),
        ],
        redirect_stdout=True,
        max_value=progressbar.UnknownLength,
    )

    monitor = LiveMonitor()
    counter = max
    inc_counter = 0

    try:
        while True:
            stamp = datetime.now(timezone.utc)

            # Calculate datetimes for the whole span of the (sub-)manifest
            (start, end, duration, delta) = calculate_hls_pdt(handler, stamp)

            attrs = [
                CL.labeled(
                    stamp.strftime("%H:%M:%S.%f"), "POLL @", label_style=CL.high2
                ),
                CL.labeled(handler.document.media_sequence, "seq"),
                CL.labeled(start, "start"),
                CL.labeled(duration, "dur"),
                CL.labeled(end, "end"),
                CL.labeled(delta, "Δ", CL.high1),
            ]
            click.echo("  ".join(attrs))

            # Extract information from current HLS document
            changes = detect_hls_signals(handler, stamp, monitor)
            # print(monitor)
            if changes["added"] and not silent:
                sound_alert(changes["added"])

                # Print new ones
                for signal in changes["added"]:
                    click.echo(
                        "  ".join(
                            [
                                CL.alert("NEW"),
                                CL.labeled(signal.type.name, "type"),
                                CL.labeled(
                                    (
                                        signal.event_type.name
                                        if signal.event_type
                                        else "-"
                                    ),
                                    "/",
                                ),
                                CL.labeled(
                                    signal.signal_time.astimezone(
                                        timezone.utc
                                    ).strftime("%H:%M:%S"),
                                    "for",
                                ),
                            ]
                        )
                    )
                    if signal.payload:
                        click.echo(CL.high3(signal.payload))
                        click.echo(("\n".join(summarize(signal.payload))))

                    click.echo(CL.expand(str(signal.content)))
                    click.echo()

            if counter == 1:
                break

            for j in range(4):
                time.sleep(int(interval) / 4)
                bar.update(
                    -counter - 1,
                    time=stamp.strftime("%H:%M:%S UTC"),
                    sequence=handler.document.media_sequence,
                )

            # time.sleep(int(interval))
            handler.reload()
            counter = counter - 1
            inc_counter = inc_counter + 1

    except KeyboardInterrupt:
        print("Stopped!")


def calculate_hls_pdt(handler: HLSHandler, now_stamp) -> Tuple[str, str, str, float]:
    start = handler.document.program_date_time
    end = handler.document.segments[-1].current_program_date_time
    end += timedelta(seconds=handler.document.segments[-1].duration)
    duration = end - start

    delta = end - now_stamp

    return (
        start.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f UTC"),
        end.astimezone(timezone.utc).strftime("%H:%M:%S.%f"),
        duration,
        delta.total_seconds(),
    )


def detect_hls_signals(handler: HLSHandler, stamp: datetime, monitor: LiveMonitor):
    with monitor as mon:
        # Detect markers
        for segment in handler.document.segments:
            # #EXT-X-DISCONTINUITY
            if segment.discontinuity:
                mon.record_signal(
                    LiveSignal(
                        type=SignalType.DISCONTINUITY,
                        appeared_at=stamp,
                        content=segment,
                        signal_time=segment.current_program_date_time,
                        event_type=(
                            EventType.AD if "/bpkio-jitt" in segment.uri else None
                        ),
                    )
                )

            # #EXT-OATCLS-SCTE35
            if segment.oatcls_scte35:
                if segment.cue_out_start:
                    mon.record_signal(
                        LiveSignal(
                            type=SignalType.SCTE35_MARKER,
                            appeared_at=stamp,
                            content=segment,
                            signal_time=segment.current_program_date_time,
                            payload=segment.oatcls_scte35,
                            event_type=EventType.CUE_OUT,
                        )
                    )
                if segment.cue_in:
                    mon.record_signal(
                        LiveSignal(
                            type=SignalType.SCTE35_MARKER,
                            appeared_at=stamp,
                            content=segment,
                            signal_time=segment.current_program_date_time,
                            payload=segment.oatcls_scte35,
                            event_type=EventType.CUE_IN,
                        )
                    )

            # #EXT-X-DATERANGES
            for daterange in segment.dateranges:
                mon.record_signal(
                    LiveSignal(
                        type=SignalType.DATERANGE,
                        appeared_at=stamp,
                        content=segment,
                        signal_time=datetime.fromisoformat(daterange.start_date),
                        payload=(
                            daterange.scte35_out
                            or daterange.scte35_in
                            or daterange.scte35_cmd
                        ),
                        event_type=(
                            EventType.CUE_IN
                            if daterange.scte35_in
                            else EventType.CUE_OUT
                        ),
                    )
                )

            # Others
            if segment.cue_in:
                mon.record_signal(
                    LiveSignal(
                        type=SignalType.SCTE35_MARKER,
                        appeared_at=stamp,
                        content=segment,
                        signal_time=segment.current_program_date_time,
                        event_type=EventType.CUE_IN,
                        # payload=segment.scte35,
                    )
                )

        return mon.changes


def sound_alert(signals: List[LiveSignal]):
    scte_signals = [
        s for s in signals if s.type in (SignalType.SCTE35_MARKER, SignalType.DATERANGE)
    ]
    if len(scte_signals):
        # only check the first signal
        if any(s for s in scte_signals if s.event_type == EventType.CUE_OUT):
            sounds.chime_up()
        elif any(s for s in scte_signals if s.event_type == EventType.CUE_IN):
            sounds.chime_down()
        else:
            sounds.chime()

    period_signals = [
        s for s in signals if s.type in (SignalType.DISCONTINUITY, SignalType.PERIOD)
    ]
    if len(period_signals):
        if any(s for s in period_signals if s.event_type == EventType.AD):
            sounds.chime_uphigh()
        else:
            sounds.chime()

    if any(s for s in signals if s not in scte_signals and s not in period_signals):
        sounds.chime()
