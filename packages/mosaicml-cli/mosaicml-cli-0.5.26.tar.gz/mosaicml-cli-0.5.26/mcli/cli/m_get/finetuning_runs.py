"""Implementation of mcli get finetuning-runs, a.k.a. mcli get ft"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generator, List, Optional

from mcli.api.exceptions import MCLIException, cli_error_handler
from mcli.api.model.finetune import Finetune
from mcli.cli.common.finetuning_run_filters import get_finetuning_runs_with_filters
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.utils.utils_date import format_timestamp
from mcli.utils.utils_run_status import RunStatus

DEFAULT_DISPLAY_LIMIT = 50

logger = logging.getLogger(__name__)


@dataclass
class FinetuningRunDisplayItem(MCLIDisplayItem):
    """Display item for finetuning runs
    """
    PROGRESS = [
        "□□□□□□□□□□", "■□□□□□□□□□", "■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□", "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□",
        "■■■■■■■■□□", "■■■■■■■■■□", "■■■■■■■■■■"
    ]

    @classmethod
    def _get_run_progress(cls, eta: datetime, start_time: datetime) -> str:
        total_time = (eta - start_time).total_seconds()
        current_time = datetime.now(timezone.utc)
        elapsed_time = (current_time - start_time).total_seconds()
        percentage = min(int((elapsed_time / total_time) * 100), 100)
        return f"{cls.PROGRESS[int(percentage / 10)]}({percentage}%)"

    @classmethod
    def from_finetuning_run(cls, finetuning_run: Finetune) -> List[MCLIDisplayItem]:
        run_rows = []
        display_status = finetuning_run.status.display_name
        execution_reason = finetuning_run.reason
        status = f"{display_status} ({execution_reason})" if execution_reason else display_status
        label = "End Time"
        if finetuning_run.status == RunStatus.RUNNING and not finetuning_run.completed_at:
            # Avoid pyright errors
            if not finetuning_run.started_at:
                raise MCLIException("started_at is None")
            label = "ETA"
            eta_suffix = ""
            if finetuning_run.estimated_end_time:
                eta_suffix = cls._get_run_progress(finetuning_run.estimated_end_time, finetuning_run.started_at)
            status = f"Running {eta_suffix}"
        run_rows.append(
            MCLIDisplayItem({
                'name':
                    finetuning_run.name,
                'ID':
                    finetuning_run.id,
                'User':
                    finetuning_run.created_by,
                'Status':
                    status,
                'Reason':
                    finetuning_run.reason,
                'Created Time':
                    format_timestamp(finetuning_run.created_at),
                label:
                    finetuning_run.estimated_end_time
                    if label == "ETA" else format_timestamp(finetuning_run.completed_at),
            }))
        return run_rows


class MCLIFinetuningRunsDisplay(MCLIGetDisplay):
    """Display manager for finetuning runs
    """

    def __init__(self, models: List[Finetune]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for model in self.models:
            items = FinetuningRunDisplayItem.from_finetuning_run(model)
            for item in items:
                yield item


@cli_error_handler('mcli get finetuning-runs')
def cli_get_finetuning_runs(
    name_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    status_filter: Optional[List[RunStatus]] = None,
    output: OutputDisplay = OutputDisplay.TABLE,
    latest: bool = False,
    user_filter: Optional[List[str]] = None,
    limit: Optional[int] = DEFAULT_DISPLAY_LIMIT,
    **kwargs,
) -> int:
    """Get a table of ongoing and completed finetuning runs
    """
    del kwargs
    finetuning_runs = get_finetuning_runs_with_filters(name_filter=name_filter,
                                                       before_filter=before_filter,
                                                       after_filter=after_filter,
                                                       status_filter=status_filter,
                                                       latest=latest,
                                                       user_filter=user_filter,
                                                       limit=limit)

    display = MCLIFinetuningRunsDisplay(finetuning_runs)
    display.print(output)
    return 0


def get_finetuning_runs_argparser(subparser: argparse._SubParsersAction):
    """Get the argparser for the ``mcli get finetuning-runs`` command
    """
    parser = subparser.add_parser('finetuning-runs',
                                  aliases=['ft'],
                                  help='Get a table of ongoing and completed finetuning runs',
                                  description='Get a table of ongoing and completed finetuning runs',
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func=cli_get_finetuning_runs)

    parser.add_argument(
        '--name',
        '-n',
        dest='name_filter',
        action='append',
        help='Filter by finetuning run name. Can be specified multiple times. '
        'If a name contains a wildcard, it must be quoted. '
        'For example: --name "my*run"',
    )
    parser.add_argument(
        '--before',
        '-b',
        dest='before_filter',
        help='Filter by finetuning runs that were created before the given timestamp. '
        'Timestamps can be specified in any format that can be parsed by the dateutil library. '
        'For example: --before "2020-01-01 12:00:00"',
    )
    parser.add_argument(
        '--after',
        '-a',
        dest='after_filter',
        help='Filter by finetuning runs that were created after the given timestamp. '
        'Timestamps can be specified in any format that can be parsed by the dateutil library. '
        'For example: --after "2020-01-01 12:00:00"',
    )
    parser.add_argument(
        '--status',
        '-s',
        dest='status_filter',
        action='append',
        choices=[s.value for s in RunStatus],
        help='Filter by finetuning run status. Can be specified multiple times. '
        'For example: --status RUNNING --status COMPLETED',
    )
    parser.add_argument(
        '--latest',
        '-l',
        dest='latest',
        action='store_true',
        help='Get only the latest finetuning run',
    )
    parser.add_argument('--user',
                        '-u',
                        dest='user_filter',
                        action='append',
                        help='Filter by user email. Can be specified multiple times. '
                        'For example: --user ')

    def limit(value: str) -> Optional[int]:
        if value.lower() == 'none':
            return None

        return int(value)

    parser.add_argument(
        '--limit',
        help='Maximum number of finetuning runs to return. Finetuning runs will be sorted by creation time. '
        f'Default: {DEFAULT_DISPLAY_LIMIT}',
        default=DEFAULT_DISPLAY_LIMIT,
        type=limit,
    )
    return parser
