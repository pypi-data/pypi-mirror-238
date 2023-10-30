import re
from dataclasses import dataclass
from datetime import datetime

from pathier import Pathier, Pathish
from typing_extensions import Self
from younotyou import younotyou

root = Pathier(__file__).parent


@dataclass
class Event:
    """Class representing a logged event."""

    level: str
    date: datetime
    message: str

    def __str__(self) -> str:
        sep = "|-|"
        return sep.join([self.level, str(self.date), self.message])


@dataclass
class Log:
    """Class representing a log file as a list of Events."""

    events: list[Event]
    path: Pathier | None = None

    def __add__(self, log: Self) -> Self:
        return Log(self.events + log.events)

    def __str__(self) -> str:
        return "\n".join(str(event) for event in self.events)

    def __getitem__(self, subscript: slice) -> Self:
        return Log(self.events[subscript], self.path)

    def __len__(self) -> int:
        return len(self.events)

    @property
    def num_events(self) -> int:
        return len(self.events)

    @staticmethod
    def _parse_events(events: list[str]) -> list[Event]:
        """Convert a list of loggi event strings into a list of `Event` objects."""
        sep = "|-|"
        to_datetime = lambda date: datetime.strptime(date, "%x %X")
        logs = []
        for event in events:
            level, date, message = event.split(sep, maxsplit=3)
            logs.append(Event(level, to_datetime(date), message))
        return logs

    @staticmethod
    def _split_log_into_events(log: str) -> list[str]:
        """Decompose a string of loggi events into a list of events, accounting for multi-line events."""
        events = []
        event = ""
        for line in log.splitlines(True):
            if re.findall("[A-Z]+\\|\\-\\|", line):
                if event:
                    events.append(event.strip("\n"))
                event = line
            else:
                event += line
        if event:
            events.append(event.strip("\n"))
        return events

    def chronosort(self):
        """Sort this object's events by date."""
        self.events = sorted(self.events, key=lambda event: event.date)

    def filter_dates(
        self, start: datetime = datetime.fromtimestamp(0), stop: datetime | None = None
    ) -> Self:
        """Returns a new `Log` object containing events between `start` and `stop`, inclusive."""
        if not stop:
            stop = datetime.now()
        return Log(
            [event for event in self.events if start <= event.date <= stop], self.path
        )

    def filter_levels(self, levels: list[str]) -> Self:
        """Returns a new `Log` object containing events with the specified levels."""
        return Log([event for event in self.events if event.level in levels], self.path)

    def filter_messages(
        self,
        include_patterns: list[str] = ["*"],
        exclude_patterns: list[str] = [],
        case_sensitive: bool = True,
    ):
        """Returns a new `Log` object containing events with messages matching those in `include_patterns`, but not matching `exclude_patterns`.

        Both lists can contain wildcard patterns."""
        return Log(
            [
                event
                for event in self.events
                if event.message
                in younotyou(
                    [event.message], include_patterns, exclude_patterns, case_sensitive
                )
            ],
            self.path,
        )

    @classmethod
    def load_log(cls, logpath: Pathish) -> Self:
        """Load a `Log` object from the log file at `logpath`."""
        logpath = Pathier(logpath)
        events = cls._split_log_into_events(logpath.read_text(encoding="utf-8"))
        return cls(cls._parse_events(events), logpath)
