""" Defines a Run Event """
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass()
class FormattedRunEvent():
    """ Formatted Run Event """
    event_type: str
    event_time: datetime
    event_message: str

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FormattedRunEvent:
        """Load the formatted run event from MAPI response.
        """
        args = {
            'event_type': response['eventType'],
            'event_time': response['eventTime'],
            'event_message': response['eventMessage'],
        }
        return cls(**args)
